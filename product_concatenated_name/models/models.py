# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.onchange('product_brand_id', 'x_studio_capacidad_de_almacenamiento', 'x_studio_modelo',
                  'x_studio_part_number', 'categ_id', 'x_studio_condition')
    def change_product_name(self):
        _logger.info("CHANGED PARAMETER")
        if self.categ_id.name == 'Teléfonos':
            name = 'Teléfono'
            brand = self.product_brand_id.name or ''
            if brand:
                name += ' ' + brand
            model = self.x_studio_modelo or ''
            if model:
                name = name + ' ' + model
            part_number = self.x_studio_part_number or ''
            if part_number:
                name += ' / ' + part_number
            capacity = self.x_studio_capacidad_de_almacenamiento.x_name or ''
            if capacity:
                name += ' / ' + capacity
            condition = self.x_studio_condition or ''
            if condition:
                name += ' / ' + condition
            self['name'] = name
