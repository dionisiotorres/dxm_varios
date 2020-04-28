# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move.line'

    functional_test_done = fields.Boolean(string='Functional Test Done')
    esthetic_test_done = fields.Boolean(string='Esthetic Test Done')
    # functional_result = fields.Selection(related='lot_id.x_studio_resultado')
    # esthetic_result = fields.Many2one(related='lot_id.x_studio_revision_grado')
