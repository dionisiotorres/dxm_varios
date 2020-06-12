# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ProductLineSpecs(models.Model):
    _name = 'product.line.specs'
    _description = 'Product line specifications'

    stock_move_line_id = fields.Many2one(comodel_name='stock.move')
    sale_order_line_id = fields.Many2one(comodel_name='sale.order.line')
    grade = fields.Many2one('x_grado', related='sale_order_line_id.product_grade')
    color = fields.Many2one(comodel_name='x_color', string='Color')
    lock_status = fields.Many2one(comodel_name='x_bloqueo', string='Lock')
    logo = fields.Many2one(comodel_name='x_logo', string="Logo")
    charger = fields.Many2one(comodel_name='x_cargador', string="Charger")
    network_type = fields.Many2one(comodel_name='x_red', string="Network")
    lang = fields.Many2one(comodel_name='x_idioma_terminal', string="Language")
    applications = fields.Many2one(comodel_name='x_terminal_aplicaciones', string="Applications")
    quantity = fields.Integer(string='Specification Quantity')
    filter_executions = fields.Integer(string='Executions')
    available_qty = fields.Integer(string='Available')

    def create_specs_filter_values(self):
        _logger.info("TRYING TO GET SPECS FILTER")
        filter_values = self.read(['color', 'logo', 'lock_status', 'charger', 'network_type',
                                   'lang', 'applications'])[0]
        filter_values.pop('id')
        _logger.info("FILTER VALUES: %r", filter_values)
        for key in filter_values.keys():
            if filter_values[key]:
                if filter_values[key][0]:
                    filter_values.update({key: filter_values[key][0]})
            # else:
            #     filter_values.pop(key)
        quant_filter = ''
        grade = self.sale_order_line_id.product_grade.id
        if grade:
            quant_filter = "q.lot_id.x_studio_revision_grado.id == %s" % grade
        operand = ' and '
        for key in filter_values:
            # grade Filter
            # if key == 'grade':
            #     if len(quant_filter) > 0:
            #         quant_filter += operand + "q.lot_id.x_studio_revision_grado.id == %s" % filter_values.get('grade')
            #     else:
            #         quant_filter = "q.lot_id.x_studio_revision_grado.id == %s" % filter_values.get('grade')

            # color Filter
            if key == 'color' and filter_values[key]:
                if len(quant_filter) > 0:
                    quant_filter += operand + "q.lot_id.x_studio_color.id == %s" % filter_values.get('color')
                else:
                    quant_filter = "q.lot_id.x_studio_color.id == %s" % filter_values.get('color')

            # lock_status Filter
            if key == 'lock_status' and filter_values[key]:
                if len(quant_filter) > 0:
                    quant_filter += operand + "q.lot_id.x_studio_bloqueo.id == %s" % filter_values.get('lock_status')
                else:
                    quant_filter = "q.lot_id.x_studio_bloqueo.id == %s" % filter_values.get('lock_status')

            # logo Filter
            if key == 'logo' and filter_values[key]:
                if len(quant_filter) > 0:
                    quant_filter += operand + "q.lot_id.x_studio_logo.id == %s" % filter_values.get('logo')
                else:
                    quant_filter = "q.lot_id.x_studio_logo.id == %s" % filter_values.get('logo')

            # charger Filter
            if key == 'charger' and filter_values[key]:
                if len(quant_filter) > 0:
                    quant_filter += operand + "q.lot_id.x_studio_cargador.id == %s" % filter_values.get('charger')
                else:
                    quant_filter = "q.lot_id.x_studio_cargador.id == %s" % filter_values.get('charger')

            # network_type Filter
            if key == 'network_type' and filter_values[key]:
                if len(quant_filter) > 0:
                    quant_filter += operand + "q.lot_id.x_studio_red.id == %s" % filter_values.get('network_type')
                else:
                    quant_filter = "q.lot_id.x_studio_red.id == %s" % filter_values.get('network_type')

            # lang Filter
            if key == 'lang' and filter_values[key]:
                if len(quant_filter) > 0:
                    quant_filter += operand + "q.lot_id.x_studio_idioma.id == %s" % filter_values.get('lang')
                else:
                    quant_filter = "q.lot_id.x_studio_idioma.id == %s" % filter_values.get('lang')

            # applications Filter
            if key == 'applications' and filter_values[key]:
                if len(quant_filter) > 0:
                    quant_filter += operand + "q.lot_id.x_studio_aplicaciones.id == %s" % filter_values.get('applications')
                else:
                    quant_filter = "q.lot_id.x_studio_aplicaciones.id == %s" % filter_values.get('applications')

        quant_filter = [self.quantity, quant_filter]

        _logger.info("SPECS FILTER RESULT: %r", quant_filter)

        return quant_filter
