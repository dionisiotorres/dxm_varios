from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    name = 'res.config.settings'
    _inherit = 'res.config.settings'

    quality_test_op_type = fields.Many2one(comodel_name='stock.picking.type',
                                           string='Quality Test Operation Type',
                                           help='In which operation type will appear this test')

    graduation_op_type = fields.Many2one(comodel_name='stock.picking.type',
                                         string='Re Graduation Operation Type',
                                         help='In which operation type will appear Re Graduation option')

    workshop_op_type = fields.Many2one(comodel_name='stock.picking.type', string='Workshop Operation Type',
                                       help='Which operation type to send devices to workshop')

    new_grade = fields.Many2one(comodel_name="x_grado",
                                string='Grade for new devices',
                                readonly=False)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            quality_test_op_type=int(get_param('mobile_device_reception.quality_test_op_type')),
            graduation_op_type=int(get_param('mobile_device_reception.graduation_op_type')),
            workshop_op_type=int(get_param('mobile_device_reception.workshop_op_type')),
            new_grade=int(get_param('mobile_device_reception.new_grade'))
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param

        quality_test_op_type = self.quality_test_op_type and self.quality_test_op_type.id or False
        graduation_op_type = self.graduation_op_type and self.graduation_op_type.id or False
        workshop_op_type = self.workshop_op_type and self.workshop_op_type.id or False
        new_grade = self.new_grade and self.new_grade.id or False

        set_param('mobile_device_reception.quality_test_op_type', quality_test_op_type)
        set_param('mobile_device_reception.graduation_op_type', graduation_op_type)
        set_param('mobile_device_reception.workshop_op_type', workshop_op_type)
        set_param('mobile_device_reception.new_grade', new_grade)
