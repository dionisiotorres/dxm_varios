from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    name = 'res.config.settings'
    _inherit = 'res.config.settings'

    delivery_op_type = fields.Many2one(comodel_name='stock.picking.type',
                                       string='Delivery Operation Type',
                                       help='Picking type for delivery operations')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            delivery_op_type=int(get_param('mobile_device_sale.delivery_op_type'))
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param

        delivery_op_type = self.delivery_op_type and self.delivery_op_type.id or False

        set_param('mobile_device_sale.delivery_op_type', delivery_op_type)
