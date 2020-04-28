from odoo import api,fields, models


class ResConfigSettings(models.TransientModel):
    name = 'res.config.settings'
    _inherit = 'res.config.settings'

    functional_test_op_type = fields.Many2one(comodel_name='stock.picking.type',
                                              string='Functional Test Operation Type',
                                              help='In which operation type will appear this test')
    esthetic_test_op_type = fields.Many2one(comodel_name='stock.picking.type', string='Esthetic Test Operation Type',
                                            help='In which operation type will appear this test')
    workshop_op_type = fields.Many2one(comodel_name='stock.picking.type', string='Workshop Operation Type',
                                       help='Which operation type to send devices to workshop')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            functional_test_op_type=int(get_param('quality_mobile_test.functional_test_op_type')),
            esthetic_test_op_type=int(get_param('quality_mobile_test.esthetic_test_op_type')),
            workshop_op_type=int(get_param('quality_mobile_test.workshop_op_type'))
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param

        functional_test_op_type = self.functional_test_op_type and self.functional_test_op_type.id or False
        esthetic_test_op_type = self.esthetic_test_op_type and self.esthetic_test_op_type.id or False
        workshop_op_type = self.workshop_op_type and self.workshop_op_type.id or False

        set_param('quality_mobile_test.functional_test_op_type', functional_test_op_type)
        set_param('quality_mobile_test.esthetic_test_op_type', esthetic_test_op_type)
        set_param('quality_mobile_test.workshop_op_type', workshop_op_type)
