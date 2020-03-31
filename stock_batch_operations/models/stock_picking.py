from odoo import models
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def unpack_lots(self):
        context = self.env.context() or {}
        _logger.info("CONTEXT: %r", [context])
        return
