# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class SerialBatchImport(models.TransientModel):
    _name = "serial.import.wizard"

    product_id = fields.Many2one(comodel_name='product.template', string='Product')
    company_id = fields.Many2one(comodel_name='res.company', string="Company")

    color = fields.Many2one(comodel_name='x_color', string="Color")
    lock_status = fields.Many2one(comodel_name='x_bloqueo', string="Lock Status")
    logo = fields.Many2one(comodel_name='x_logo', string="Logo")
    charger = fields.Many2one(comodel_name='x_cargador', string="Charger")

    network_type = fields.Many2one(comodel_name='x_red', string="Network Type")
    lang = fields.Many2one(comodel_name='x_idioma', string="Language")
    memory = fields.Many2one(comodel_name='x_memoria', string="Memory")
    sim_type = fields.Many2one(comodel_name='x_tipo_de_sim', string="SIM Type")
    display = fields.Many2one(comodel_name='x_pantalla', string="Display")
    release = fields.Many2one(comodel_name='x_lanzamiento', string="Release")

    serial_file = fields.Binary(string="File")

    def _import_serial(self):
        pass

