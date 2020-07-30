# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    stock_qty = fields.Float(string="Real Quantity in Stock", compute="_get_product_stock")

    def _get_product_stock(self):
        company_id = self.env.user.company_id
        warehouse_id = self.env['stock.warehouse'].sudo().search([('company_id', '=', company_id.id)])
        stock_location = warehouse_id.lot_stock_id

        for template in self:
            template_quants = self.env['stock.quant'].sudo()._gather(template.product_variant_id, stock_location)
            template.stock_qty = len(template_quants)
