# -*- coding: utf-8 -*-

from odoo import fields, models


class MessagePopup(models.TransientModel):
    _name = "message.popup"

    name = fields.Text(string="Message")

    def popup(self, message_type='success', message=False):
        msg = self.create({'name': message})
        if message_type == 'success':
            message_type = '<i class="fa fa-thumbs-o-up"/> Success'
        elif message_type == 'warning':
            message_type = '<i class="fa fa-warning"/> Warning'
        elif message_type == 'error':
            message_type = '<i class="fa fa-thumbs-o-down"/> Error'
        elif message_type == 'info':
            message_type = '<i class="fa fa-info-circle"/> Info'

        return {
            'name': message_type,
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'message.popup',
            'res_id': msg.id,
            'view_id': False,
            'target': 'new',
        }


class ResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    def test_popup(self):
        return self.env['message.popup'].popup(message_type="success", message="Success message example.")
