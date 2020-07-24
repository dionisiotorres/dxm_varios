# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def get_similar_barcode(self):
        picking = self
        lots = []
        company_id = self.env.user.company_id
        warehouse_id = self.env['stock.warehouse'].sudo().search([('company_id', '=', company_id.id)])
        stock_location = warehouse_id.lot_stock_id
        _logger.info("PICKING: %r", picking)
        for line in picking.move_lines:
            product_quants = self.env['stock.quant'].sudo()._gather(line.product_id, stock_location)
            for specs in line.mapped('move_line_specs_ids'):
                specs_filter = specs.create_specs_filter_values()[1]
                _logger.info("SPECS FILTER: %r", specs_filter)
                quant_filtered = product_quants.filtered(lambda q: eval(specs_filter))
                lots_in_quants = quant_filtered.mapped('lot_id').ids
                lots += lots_in_quants

        return lots
