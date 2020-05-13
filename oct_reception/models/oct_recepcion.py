# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError


class ControlRecipientPackages(models.Model):
    _name = "control.recipient.packages"

    date_in = fields.Date(string="Fecha de ingreso")
    name = fields.Char('Name', copy=False, readonly=True, default=lambda x: _('New'))
    origin = fields.Char(string="Expedición")
    carrier = fields.Char(string="Transportista")
    note = fields.Char(string="Observaciones")
    # line_ids = fields.One2many('recipient.lines', 'recipient_id')
    # state = fields.Selection([
    #     ('new', 'New'),
    #     ('received', 'Received')], default='new')
    picking_ids = fields.One2many('stock.picking', 'recipient_id', string="Pickings")
    company_id = fields.Many2one('res.company',
                                 string='Company',
                                 required=True,
                                 index=True,
                                 default=lambda self: self.env.user.company_id,
                                 help="Company related to this journal")
    picking_count = fields.Integer(compute='_compute_picking_count')
    packages = fields.Integer(string="Package Quantity")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Provider")

    def _compute_picking_count(self):
        for package in self:
            package.picking_count += len(package.picking_ids)

    @api.model
    def create(self, vals):
        if not vals.get('name', False) or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('control.recipient.packages') or _('New')
        return super(ControlRecipientPackages, self).create(vals)

    # def action_create_picking(self):
    #     view = self.env.ref('stock.view_picking_form')
    #     picking_type_id = self.env.ref('stock.picking_type_in').id
    #     return {
    #         'name': _('Stock Picking'),
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'stock.picking',
    #         'view_id': view.id,
    #         'type': 'ir.actions.act_window',
    #         'context': {'default_picking_type_id': picking_type_id,
    #                     'default_recipient_id': self.id, 'default_origin': self.name},
    #     }

    def action_view_picking(self):
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        if self.picking_count > 1:
            action['domain'] = "[('id', 'in', %s)]" % self.picking_ids.ids
        elif self.picking_count == 1:
            action['views'] = [(self.env.ref('stock.view_picking_form').id or False, 'form')]
            action['res_id'] = self.picking_ids[0].id
        return action


# class RecipientLines(models.Model):
#     _name = "recipient.lines"
#
#     recipient_id = fields.Many2one('control.recipient.packages')
#     height = fields.Float(string="Height")
#     width = fields.Float(string="Width")
#     depth = fields.Float(string="Depth")
#     uom_id = fields.Many2one('uom.uom', string="UoM")
#     note = fields.Char(string='Note')
#     partner_id = fields.Many2one('res.partner', string='Partner')


class StockPicking(models.Model):
    _inherit = "stock.picking"

    recipient_id = fields.Many2one('control.recipient.packages', string="Recipient")
