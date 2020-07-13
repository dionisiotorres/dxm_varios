# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    weight = fields.Float(string="Weight")
    dimension = fields.Char(string="Dimension")
    pallet_type = fields.Selection(selection=[('s', _('Standard Pallet')),
                                              ('u', _('Universal Pallet')),
                                              ('e', _('EuroPallet'))], string="Pallet Type")
    package_qty = fields.Integer(string="Package Quantity")
    pickup_address = fields.Char(string="Pickup Address")
    contact_name = fields.Char(string="Contact")
    weight_uom = fields.Char(compute="_get_wight_uom_name")

    def _get_wight_uom_name(self):
        uom_name = None
        get_param = self.env['ir.config_parameter'].sudo().get_param
        product_weight_in_lbs_param = get_param('product.weight_in_lbs')
        if product_weight_in_lbs_param == '1':
            uom_name = self.env.ref('uom.product_uom_lb', False).name or self.env['uom.uom'].search(
                [('measure_type', '=', 'weight'), ('uom_type', '=', 'reference')], limit=1).name
        else:
            uom_name = self.env.ref('uom.product_uom_kgm', False).name or self.env['uom.uom'].search(
                [('measure_type', '=', 'weight'), ('uom_type', '=', 'reference')], limit=1).name

        for record in self:
            record["weight_uom"] = uom_name

