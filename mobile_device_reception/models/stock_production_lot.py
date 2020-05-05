# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class Picking(models.Model):
    _inherit = "stock.production.lot"

    esthetic_test_id = fields.Many2one(comodel_name="esthetic.quality.test")
    functional_test_id = fields.Many2one(comodel_name="functional.quality.test")
