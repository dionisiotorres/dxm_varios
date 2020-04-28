# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import xlrd
import logging

_logger = logging.getLogger(__name__)


class FunctionalTest(models.TransientModel):
    _name = 'mobile.esthetic.test.wizard'
    _inherit = 'esthetic.quality.test'
    _description = 'Esthetic test'

    serial_file = fields.Binary(string="File")

    @api.onchange('lot_id')
    def onchange_lot_id(self):
        if self.lot_id:
            piking_id = self.env.context.get('active_id')
            move_ids = self.env['stock.picking'].search([('id', '=', piking_id)]).move_line_ids
            move = move_ids.filtered(lambda move_line: move_line.lot_id.name == self.lot_id)
            if move:
                self.update({'move_ids': [(4, move.id, 0)]})
            else:
                raise ValidationError("No move line found with lot %s" % self.lot_id)
            self.lot_id = False

    @api.onchange('serial_file')
    def onchange_serial_file(self):
        if self.serial_file:
            piking_id = self.env.context.get('active_id')
            move_ids = self.env['stock.picking'].search([('id', '=', piking_id)]).move_line_ids
            # process the .xls file
            file_decoded = base64.decodebytes(self.serial_file)
            book = xlrd.open_workbook(file_contents=file_decoded)
            sheet = book.sheet_by_index(0)
            serial_values = []
            for rowx, row in enumerate(map(sheet.row, range(sheet.nrows)), 1):
                for colx, cell in enumerate(row, 1):
                    serial_values.append(cell.value)
            for serial in serial_values:
                move = move_ids.filtered(lambda move_line: move_line.lot_id.name == serial)
                if move:
                    self.update({'move_ids': [(4, move.id, 0)]})

    def process_test(self):
        _logger.info("RUNNING FUNCTIONAL TEST")
        esthetic_test_obj = self.env['esthetic.quality.test']
        exclude_fields = ['id', 'display_name', 'create_uid', 'create_date', 'write_uid',
                          'write_date', '__last_update', 'serial_file']
        fields_esthetic_to_read = [
            element for element in esthetic_test_obj.fields_get_keys() if element not in exclude_fields
        ]
        esthetic_test_values = self.read(fields_esthetic_to_read)[0]
        esthetic_test_values.pop('id')
        _logger.info(esthetic_test_values)
        test_obj = esthetic_test_obj.create(esthetic_test_values)
        test_result = test_obj.get_esthetic_result()
        test_obj.write({'test_result': test_result})
        grado = self.env['x_grado'].search([('x_name', '=', test_result)])
        for line in test_obj.move_ids:
            line.write({'esthetic_test_done': True})
            line.lot_id.write({
                'x_studio_revision_estetica': True,
                'x_studio_revision_grado': grado.id,
                'esthetic_test': test_obj.id,
            })
        message = self.env['message.popup']
        text_message = 'Esthetic test is <strong>%s</strong> for %s lots' % (test_result, len(self.move_ids))
        return message.popup(message=text_message)
