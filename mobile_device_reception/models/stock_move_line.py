# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move.line'

    quality_test_done = fields.Boolean(string='Quality Test Done')
