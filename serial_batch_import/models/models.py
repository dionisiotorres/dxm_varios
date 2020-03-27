# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import xlrd
import logging

_logger = logging.getLogger(__name__)


class SerialBatchImport(models.TransientModel):
    _name = "serial.import.wizard"

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
    memory = fields.Many2one(comodel_name='x_memoria.ram', string="Memory")
    sim_type = fields.Many2one(comodel_name='x_tipo_de_sim', string="SIM Type")
    display = fields.Many2one(comodel_name='x_pantalla', string="Display")
    release = fields.Many2one(comodel_name='x_lanzamiento.terminal', string="Release")

    serial_file = fields.Binary(string="File")

    def import_serial(self):
        context = self.env.context.copy() or {}
        picking_id = context.get('active_id')
        stock_picking = self.env['stock.picking'].search([('id', '=', picking_id)])
        # process the .xls file
        file_decoded = base64.decodebytes(self.serial_file)
        book = xlrd.open_workbook(file_contents=file_decoded)
        sheet = book.sheet_by_index(0)
        serial_values = []
        for rowx, row in enumerate(map(sheet.row, range(sheet.nrows)), 1):
            for colx, cell in enumerate(row, 1):
                serial_values.append(cell.value)
        lot_obj = self.env['stock.production.lot']
        # get the move lines on picking for this product with no lot_id
        move_lines = self.env['stock.move.line'].search([('picking_id', '=', stock_picking.id), ('lot_id', '=', False),
                                                         ('product_id', '=', self.product_id.product_variant_id.id)])
        if len(serial_values) <= len(move_lines):
            for serial_by_moveline in zip(serial_values, move_lines):
                lot_values = {
                    'name': serial_by_moveline[0],
                    'product_id': self.product_id.id,
                    'company_id': self.company_id.id,
                    'x_studio_part_number': self.product_id.x_studio_part_number,  # Part Number
                    'x_studio_capacidad': self.product_id.x_studio_capacidad.id,  # Capacidad
                    'x_studio_grado_preliminar': self.product_id.x_studio_grado_preliminar.id,  # Grado
                    'x_studio_color': self.color.id,  # Color
                    'x_studio_bloqueo': self.lock_status.id,  # Bloqueo
                    'x_studio_logo': self.logo.id,  # Logo
                    'x_studio_cargador': self.charger.id,  # Cargador
                    'x_studio_red': self.network_type.id,  # Red
                    'x_studio_idioma': self.lang.id,  # Idioma
                    'x_studio_memoria_ram': self.memory.id,  # Memoria
                    'x_studio_tipo_de_sim': self.sim_type.id,  # Tipo de SIM
                    'x_studio_tamao_de_pantalla': self.display.id,  # Pantalla
                    'x_studio_fecha_de_lanzamiento': self.release.id  # Lanzamiento
                }
                lot_id = lot_obj.create(lot_values)
                serial_by_moveline[1].write({'lot_id': lot_id.id, 'qty_done': serial_by_moveline[1].product_uom_qty})
            self._cr.commit()
            message_popup = self.env['message.popup']
            return message_popup.popup(message=_(
                "%s serial(s) imported successfully to product %s" % (len(serial_values), self.product_id.name)))

        else:
            raise UserError(
                _("The quantity (%s) of serial numbers don't match with the quantity (%s) of move lines to process. "
                  "You must provide the same or less number of serial as movement lines" % (len(serial_values),
                                                                                            len(move_lines))))
