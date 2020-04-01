from odoo import models, fields
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _check_package_to_unpack(self):
        for picking in self:
            result = False
            for move in picking.move_line_ids:
                if move.result_package_id:
                    result = True
            picking.need_unpack = result

    need_unpack = fields.Boolean(compute='_check_package_to_unpack')

    def unpack_lots(self):
        packages = []
        qties = 0
        _logger.info("PICKING ID: %r", [self.id])
        for move in self.move_line_ids:
            if move.result_package_id:
                move.write({'result_package_id': [(3, move.result_package_id.id, 0)]})
                packages.append(move.result_package_id.id)
                qties += move.product_qty
        number_of_packages = len(set(packages))
        message = self.env['message.popup']
        product_term = message.pluralize(qties, 'product', 'products')
        packages_term = message.pluralize(number_of_packages, 'package', 'packages')
        return message.popup(message="%s unpacked from %s" % (product_term, packages_term))
