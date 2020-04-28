# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import xlrd
import logging

_logger = logging.getLogger(__name__)


class FunctionalTest(models.TransientModel):
    _name = 'mobile.functional.test.wizard'
    _inherit = 'functional.quality.test'
    _description = 'Functional test'

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
        functional_test_obj = self.env['functional.quality.test']
        exclude_fields = ['id', 'display_name', 'create_uid', 'create_date', 'write_uid',
                          'write_date', '__last_update', 'serial_file']
        fields_to_read = [element for element in self.fields_get_keys() if element not in exclude_fields]
        functional_test_values = self.read(fields_to_read)[0]
        functional_test_values.pop('id')
        _logger.info(functional_test_values)
        test_obj = functional_test_obj.create(functional_test_values)
        test_result = test_obj.get_functional_result()
        test_obj.write({'test_pass': test_result})
        for line in test_obj.move_ids:
            line.write({'functional_test_done': True})
            line.lot_id.write({
                'x_studio_revision_funcional': True,
                'x_studio_resultado': 'Sin averia' if test_result else 'Con averia',
                'functional_test': test_obj.id
            })
        message = self.env['message.popup']
        text_message = 'Functional test %s for %s lots' % ('passed' if test_result else 'not passed',
                                                           len(self.move_ids))
        return message.popup(message=text_message)
