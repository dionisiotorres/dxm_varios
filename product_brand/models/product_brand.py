# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductBrand(models.Model):
    _name = 'product.brand'

    name = fields.Char(string='Brand Name')
    product_ids = fields.One2many(comodel_name='product.template', inverse_name='product_brand_id')
    product_count = fields.Integer(compute='_count_products')

    def _count_products(self):
        for record in self:
            if len(record.product_ids) > 0:
                record.product_count = len(record.product_ids)
            else:
                record.product_count = 0
