# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    label_paper_format = fields.Many2one(comodel_name='report.paperformat', string='Product Label Paper format')
    label_report_layout_id = fields.Many2one('ir.ui.view', 'Label Template')
