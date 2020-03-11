# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # def _get_display_name(self):
    #    for record in self:
    #        name_prefix = 'Teléfono'
    #        brand = record.x_studio_field_LBIjI.x_name or ''
    #        model = record.x_studio_modelo or ''
    #        part_number = record.x_studio_part_number or ''
    #        capacity = record.x_studio_field_t1rly.display_name or ''
    #        grade = record.x_studio_field_3tFsU.display_name or ''
    #        if brand and model and part_number and capacity and grade:
    #            record.display_name =  name_prefix + ' ' + brand + ' ' + model + ' / ' + part_number + ' / ' + capacity + ' - ' + grade
    #        else:
    #            record.display_name = record.name

    # display_name = fields.Char(compute=_get_display_name)

    # def name_get(self):
    #    display_name = []
    #    for record in self:
    #        name_prefix = 'Teléfono'
    #        brand = record.x_studio_field_LBIjI.x_name or ''
    #        model = record.x_studio_modelo or ''
    #        part_number = record.x_studio_part_number or ''
    #       capacity = record.x_studio_field_t1rly.display_name or ''
    #        grade = record.x_studio_field_3tFsU.display_name or ''
    #        name = name_prefix + ' ' + brand + ' ' + model + ' / ' + part_number + ' / ' + capacity + ' - ' + grade
    #        display_name.append((record.id, name))
    #    return display_name

    # Marca, Modelo, Part number, Capacity, Grade
    @api.onchange('x_studio_field_LBIjI', 'x_studio_modelo', 'x_studio_part_number', 'x_studio_field_t1rly',
                  'x_studio_field_3tFsU', 'categ_id')
    def change_product_name(self):
        if self.categ_id.name == 'Teléfonos':
            name = 'Teléfono'
            brand = self.x_studio_field_LBIjI.x_name or ''
            if brand:
                name += ' ' + brand
            model = self.x_studio_modelo or ''
            if model:
                name = name + ' ' + model
            part_number = self.x_studio_part_number or ''
            if part_number:
                name += ' / ' + part_number
            capacity = self.x_studio_field_t1rly.display_name or ''
            if capacity:
                name += ' / ' + capacity
            grade = self.x_studio_field_3tFsU.display_name or ''
            if grade:
                name += ' - ' + grade
            self.name = name
