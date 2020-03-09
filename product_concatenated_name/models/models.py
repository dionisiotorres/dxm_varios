# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.onchange('brand')
    def change_product_name(self):
        pass
