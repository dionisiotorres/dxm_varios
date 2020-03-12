# -*- coding: utf-8 -*-

from odoo import fields, models


class MessagePopup(models.TransientModel):
    _name = "message.popup"

    name = fields.Text(string="Message")

    def popup(self, message_type='Success', message=False):
        msg = self.create({'name': message})
        return {
            'name': message_type,
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'message.popup',
            'res_id': msg.id,
            'view_id': False,
            'nodestroy': True,
            'target': 'new',
            'domain': [],
        }
