# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Brand, Model, Part number, Capacity, Grade
    @api.onchange('x_studio_field_LBIjI',
                  'x_studio_modelo',
                  'x_studio_part_number',
                  'x_studio_field_t1rly',
                  'x_studio_field_3tFsU')
    def change_product_name(self):
        name_prefix = 'Teléfono'
        brand = self.x_studio_field_LBIjI.x_name or ''
        model = self.x_studio_modelo or ''
        part_number = self.x_studio_part_number or ''
        capacity = self.x_studio_field_t1rly.display_name or ''
        grade = self.x_studio_field_3tFsU.display_name or ''
        if brand and model and part_number and capacity and grade:
            self.name = name_prefix + ' ' + brand + ' ' + model + ' / ' + part_number + ' / ' + capacity + ' - ' + grade
