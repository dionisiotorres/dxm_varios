# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import xlrd
import logging

_logger = logging.getLogger(__name__)


class FunctionalTest(models.TransientModel):
    _name = 'mobile.quality.test.wizard'
    _inherit = ['functional.quality.test', 'esthetic.quality.test']
    _description = 'Quality test'

    # Serial Batch Import

    def _get_current_company(self):
        return self.env.company.id

    def _get_product_domain(self):
        context = self.env.context.copy() or {}
        picking_id = context.get('active_id')
        picking = self.env['stock.picking'].search([('id', '=', picking_id)])
        ids = picking.move_ids_without_package.product_id.ids
        return [('id', 'in', ids)]

    company_id = fields.Many2one(comodel_name='res.company', string="Company", default=_get_current_company)
    product_id = fields.Many2one(comodel_name='product.product', string='Product', domain=_get_product_domain)
    color = fields.Many2one(comodel_name='x_color', string="Color")
    lock_status = fields.Many2one(comodel_name='x_bloqueo', string="Lock Status")
    logo = fields.Many2one(comodel_name='x_logo', string="Logo")
    charger = fields.Many2one(comodel_name='x_cargador', string="Charger")
    network_type = fields.Many2one(comodel_name='x_red', string="Network Type")
    lang = fields.Many2one(comodel_name='x_idioma_terminal', string="Language")
    applications = fields.Many2one(comodel_name='x_terminal_aplicaciones', string="Applications")

    serial_file = fields.Binary(string="File")
    lot_id = fields.Char(string="Find Lot")
    new_lot_ids = fields.Many2many(comodel_name='stock.production.lot')

    @api.depends('product_id', 'company_id')
    @api.onchange('lot_id')
    def onchange_lot_id(self):
        if self.lot_id and self.product_id and self.company_id:
            piking_id = self.env.context.get('active_id')
            picking = self.env['stock.picking'].browse(piking_id)
            move_qty = picking.move_lines.filtered(lambda m: m.product_id.id == self.product_id.id).product_uom_qty
            lots_done = len(self.new_lot_ids)
            # First check if there is more product qty to supply a lot id
            if lots_done < move_qty:
                # Then create the lot
                existing_lot = self.env['stock.production.lot'].search([('name', '=', self.lot_id)])
                existing_lot_processed = self.env['stock.move.line'].search([('lot_id.name', '=', self.lot_id),
                                                                             ('picking_id', '!=', piking_id)])
                if not existing_lot:
                    lot_value = {
                        'name': self.lot_id,
                        'product_id': self.product_id.id,
                        'company_id': self.company_id.id
                    }
                    lot = self.env['stock.production.lot'].create(lot_value)
                    self.update({'new_lot_ids': [(4, lot.id, 0)]})
                elif existing_lot and not existing_lot_processed:
                    self.update({'new_lot_ids': [(4, existing_lot.id, 0)]})
                elif existing_lot and existing_lot_processed:
                    raise ValidationError("The lot %s have been processed. Lots must be unique" % self.lot_id)
            else:
                raise ValidationError("You can't process more lot quantities than product quantities. You have %s lots "
                                      "for %s products to process" % (lots_done, move_qty))
            self.lot_id = False

    @api.depends('product_id', 'company_id')
    @api.onchange('serial_file')
    def onchange_serial_file(self):
        if self.serial_file and self.product_id and self.company_id:
            piking_id = self.env.context.get('active_id')
            picking = self.env['stock.picking'].browse(piking_id)
            move_qty = picking.move_lines.filtered(lambda m: m.product_id.id == self.product_id.id).product_uom_qty
            lots_done = len(self.new_lot_ids)
            # process the .xls file
            file_decoded = base64.decodebytes(self.serial_file)
            book = xlrd.open_workbook(file_contents=file_decoded)
            sheet = book.sheet_by_index(0)
            serial_values = []
            for rowx, row in enumerate(map(sheet.row, range(sheet.nrows)), 1):
                for colx, cell in enumerate(row, 1):
                    serial_values.append(cell.value)
            # First check if there is more product qty to supply a lot id
            if lots_done < move_qty:
                lots_to_fill = move_qty - lots_done
                # Check if the product qty to fill a lot is greater or equal than number of serials uploaded
                if lots_to_fill >= len(serial_values):
                    # Then create the lots
                    for serial in serial_values:
                        existing_lot = self.env['stock.production.lot'].search([('name', '=', serial)])
                        existing_lot_processed = self.env['stock.move.line'].search([('lot_id.name', '=', serial),
                                                                                     ('picking_id', '!=', piking_id)])
                        if not existing_lot:
                            lot_value = {
                                'name': serial,
                                'product_id': self.product_id.id,
                                'company_id': self.company_id.id
                            }
                            lot = self.env['stock.production.lot'].create(lot_value)
                            self.update({'new_lot_ids': [(4, lot.id, 0)]})
                        elif existing_lot and not existing_lot_processed:
                            self.update({'new_lot_ids': [(4, existing_lot.id, 0)]})
                        elif existing_lot and existing_lot_processed:
                            raise ValidationError("The lot %s have been processed. Lots must be unique" % serial)
                else:
                    raise ValidationError(
                        "You can't process more lot quantities than product quantities. You have uploaded %s lots "
                        "to process %s products" % (len(serial_values), lots_to_fill))
            else:
                raise ValidationError("You can't process more lot quantities than product quantities. "
                                      "You have uploaded %s lots to process %s products" % (lots_done, move_qty))

    def process_test(self):
        _logger.info("RUNNING FUNCTIONAL TEST")
        functional_test_obj = self.env['functional.quality.test']
        esthetic_test_obj = self.env['esthetic.quality.test']

        exclude_fields = ['id', 'display_name', 'create_uid', 'create_date', 'write_uid',
                          'write_date', '__last_update', 'serial_file', 'lot_id',
                          'new_lot_ids', 'company_id', 'product_id']

        functional_fields = [element for element in
                             functional_test_obj.fields_get_keys() if element not in exclude_fields]
        esthetic_fields = [element for element in
                           esthetic_test_obj.fields_get_keys() if element not in exclude_fields]

        functional_test_values = self.read(functional_fields)[0]
        functional_test_values.pop('id')

        esthetic_test_values = self.read(esthetic_fields)[0]
        esthetic_test_values.pop('id')

        _logger.info(functional_test_values)
        _logger.info(esthetic_test_values)

        functional_obj = functional_test_obj.create(functional_test_values)
        _logger.info("FUNCTIONAL RESULT ON WIZARD: %r", functional_obj.test_pass)
        esthetic_obj = esthetic_test_obj.create(esthetic_test_values)
        grade_object = self.env['x_grado'].search([('x_name', '=', esthetic_obj.test_result)])
        for lot in self.new_lot_ids:

            lot.write({
                # Specifications
                'x_studio_color': self.color.id,
                'x_studio_bloqueo': self.lock_status.id,
                'x_studio_red': self.network_type.id,
                'x_studio_logo': self.logo.id,
                'x_studio_idioma': self.lang.id,
                'x_studio_cargador': self.charger.id,
                'x_studio_aplicaciones': self.applications.id,
                # Test
                'esthetic_test_id': esthetic_obj.id,
                'functional_test_id': functional_obj.id,
                'x_studio_revision_estetica': True,
                'x_studio_revision_grado': grade_object.id,
                'x_studio_revision_funcional': True,
                'x_studio_resultado': 'Sin averia' if functional_obj.test_pass else 'Con averia',
            })

        piking_id = self.env.context.get('active_id')
        picking = self.env['stock.picking'].browse(piking_id)
        move_lines = picking.move_line_ids.filtered(
            lambda m: m.product_id.id == self.product_id.id
        )
        processing_lot_ids = self.new_lot_ids.ids
        for move in move_lines:
            if move.lot_id.id:
                if move.lot_id.id in processing_lot_ids:
                    processing_lot_ids.remove(move.lot_id.id)
                    # move.write({
                    #     'quality_test_done': True,
                    # })
        move_lines_no_lot = picking.move_line_ids.filtered(
            lambda m: m.product_id.id == self.product_id.id and not m.lot_id
        )
        for move_by_lot in zip(processing_lot_ids, move_lines_no_lot):
            move_by_lot[1].write({
                    'quality_test_done': True,
                    'lot_id': move_by_lot[0],
                    'qty_done': 1
                })

        message = self.env['message.popup']
        text_message = '%s lots processed ' % len(self.new_lot_ids)
        return message.popup(message=text_message)
