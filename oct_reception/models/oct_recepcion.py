# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ControlRecipientPackages(models.Model):
    _name = "control.recipient.packages"

    date_in = fields.Datetime(string="Date In")
    name = fields.Char('Name', copy=False, readonly=True, default=lambda x: _('New'))
    origin = fields.Char(string="Expedition")
    carrier = fields.Char(string="Carrier")
    note = fields.Char(string="Note")
    picking_ids = fields.One2many('stock.picking', 'recipient_id', string="Pickings")
    company_id = fields.Many2one('res.company',
                                 string='Company',
                                 required=True,
                                 index=True,
                                 default=lambda self: self.env.user.company_id,
                                 help="Company related to this reception")
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

    def action_view_picking(self):
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        if self.picking_count > 1:
            action['domain'] = "[('id', 'in', %s)]" % self.picking_ids.ids
        elif self.picking_count == 1:
            action['views'] = [(self.env.ref('stock.view_picking_form').id or False, 'form')]
            action['res_id'] = self.picking_ids[0].id
        return action


class StockPicking(models.Model):
    _inherit = "stock.picking"

    recipient_id = fields.Many2one('control.recipient.packages', string="Recipient")
