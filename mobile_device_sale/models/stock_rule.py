# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):
        move_values = super(StockRule, self)._get_stock_move_values(product_id,
                                                                    product_qty,
                                                                    product_uom,
                                                                    location_id,
                                                                    name,
                                                                    origin,
                                                                    company_id,
                                                                    values)
        sale_line_id = values.get('sale_line_id')
        sale_line_obj = self.env['sale.order.line'].search([('id', '=', sale_line_id)])
        specs_lines_ids = sale_line_obj.line_specs_ids.ids
        _logger.info("SPECS IDS: %r", specs_lines_ids)
        _logger.info("MOVE VALUES: %r", values)
        if specs_lines_ids:
            move_values['move_line_specs_ids'] = [(4, spec_id) for spec_id in specs_lines_ids]
        elif not specs_lines_ids:
            _logger.info("NOT SPECS LINE")
            if sale_line_obj.product_grade:
                _logger.info("LINE WITH GRADE")
                specs_values = {'sale_order_line_id': sale_line_obj.id, 'quantity': sale_line_obj.product_uom_qty}
                new_specs = self.env['product.line.specs'].create(specs_values)
                move_values['move_line_specs_ids'] = [(4, new_specs.id)]
        return move_values
