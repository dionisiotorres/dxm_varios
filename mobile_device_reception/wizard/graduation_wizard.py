# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import base64
import xlrd
import logging

_logger = logging.getLogger(__name__)


class GraduationWizard(models.TransientModel):
    _name = 'graduation.wizard'
    _description = 'Graduation wizard'

    new_grade = fields.Many2one(comodel_name="x_grado", string="New Grade")
    lot_ids = fields.Many2many(comodel_name='stock.production.lot')
    lot_id = fields.Char(string="Search Lot")
    serial_file = fields.Binary(string="File")

    @api.onchange('lot_id')
    def onchange_lot_id(self):
        if self.lot_id:
            piking_id = self.env.context.get('active_id')
            picking = self.env['stock.picking'].browse(piking_id)
            move = picking.move_line_ids.filtered(lambda m: m.lot_id.name == self.lot_id)
            if move:
                self.update({'lot_ids': [(4, move.lot_id.id, 0)]})
            else:
                raise ValidationError("Lot %s not found in this stock move" % self.lot_id)
            self.lot_id = False

    @api.onchange('serial_file')
    def onchange_serial_file(self):
        if self.serial_file:
            piking_id = self.env.context.get('active_id')
            picking = self.env['stock.picking'].browse(piking_id)
            # process the .xls file
            file_decoded = base64.decodebytes(self.serial_file)
            book = xlrd.open_workbook(file_contents=file_decoded)
            sheet = book.sheet_by_index(0)
            serial_values = []
            for rowx, row in enumerate(map(sheet.row, range(sheet.nrows)), 1):
                for colx, cell in enumerate(row, 1):
                    serial_values.append(cell.value)
            if serial_values:
                for serial in serial_values:
                    move = picking.move_line_ids.filtered(lambda m: m.lot_id.name == serial)
                    if move:
                        self.update({'lot_ids': [(4, move.lot_id.id, 0)]})
                    else:
                        raise ValidationError("Lot %s not found in this stock move" % self.lot_id)
            else:
                raise ValidationError("No serials found to process in this file")

    def process_lots(self):
        graduation_op_id = int(self.env['ir.config_parameter'].sudo().get_param(
            'mobile_device_reception.graduation_op_type'))
        operation_type_obj = self.env['stock.picking.type'].browse(graduation_op_id)
        piking_id = self.env.context.get('active_id')
        picking = self.env['stock.picking'].browse(piking_id)
        if graduation_op_id == picking.picking_type_id.id:
            for lot in self.lot_ids:
                lot.write({
                    'x_studio_revision_grado': self.new_grade.id
                })
        else:
            raise ValidationError("You can run this action only in operations type %s" % operation_type_obj.name)
