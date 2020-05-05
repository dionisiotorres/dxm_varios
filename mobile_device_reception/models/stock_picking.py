# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class Picking(models.Model):
    _inherit = "stock.picking"

    quality_test_done = fields.Boolean(string='All Quality Test Done', compute='_check_quality_test_done')

    show_quality_test = fields.Boolean(compute="_show_quality_test")

    def _show_quality_test(self):
        q_test_id = self.env['ir.config_parameter'].sudo().get_param('mobile_device_reception.quality_test_op_type')
        for picking in self:
            if q_test_id:
                if int(q_test_id) == picking.picking_type_id.id:  # picking.company_id.functional_test_op_type
                    picking.show_quality_test = True
                else:
                    picking.show_quality_test = False
            else:
                picking.show_quality_test = False

    def _check_quality_test_done(self):
        for picking in self:
            test_done = True
            for move_line in picking.move_line_ids:
                if not move_line.quality_test_done:
                    test_done = False
            picking.quality_test_done = test_done

    def button_validate(self):
        q_test_id = int(self.env['ir.config_parameter'].sudo().get_param(
            'mobile_device_reception.quality_test_op_type'
        ))
        if self.picking_type_id.id == q_test_id:
            if not self.quality_test_done:
                raise ValidationError("You must run quality test in all lots to validate this picking.")
            else:
                # First check if there is move lines to SAT location.
                move_to_workshop = self._check_workshop_lines()
                if move_to_workshop:
                    self._create_workshop_move()
                return super(Picking, self).button_validate()
        else:
            return super(Picking, self).button_validate()

    def _check_workshop_lines(self):
        workshop_lines = self.move_line_ids.filtered(
            lambda move_line: move_line.lot_id.x_studio_resultado == 'Con averia'
        )
        if workshop_lines:
            return True
        else:
            return False

    def _create_workshop_move(self):
        workshop_op_type = int(self.env['ir.config_parameter'].sudo().get_param(
            'mobile_device_reception.workshop_op_type'
        ))
        op_type = self.env['stock.picking.type'].browse(workshop_op_type)
        workshop_picking = self.env['stock.picking']
        for picking in self:
            move_lines_to_workshop = picking.move_line_ids.filtered(
                lambda l: l.lot_id.x_studio_resultado == 'Con averia'
            )
            if move_lines_to_workshop:
                ws_picking = picking.copy({
                    'name': '/',
                    'move_lines': [],
                    'move_line_ids': [],
                    'picking_type_id': workshop_op_type,
                    'location_dest_id': op_type.default_location_dest_id.id
                })
                move_map = {}
                for move_line in move_lines_to_workshop:
                    move_id = move_line.move_id.id
                    if move_id in move_map.keys():
                        map_ids = move_map.get(move_id)
                        map_ids.append(move_line.id)
                        move_map.update({move_id: map_ids})
                    else:
                        move_map[move_id] = [move_line.id]
                _logger.info(move_map)
                for move in move_map:
                    picking_move = picking.move_lines.filtered(lambda m: m.id == move)
                    split_qty = len(move_map.get(move))
                    workshop_move_id = picking_move._split(split_qty)
                    workshop_move = self.env['stock.move'].search([('id', '=', workshop_move_id)])
                    workshop_move.write({
                        'picking_id': ws_picking.id,
                        'location_dest_id': ws_picking.location_dest_id.id,
                        'state': 'assigned'
                    })
                    workshop_lines = move_lines_to_workshop.filtered(lambda m: m.id in move_map.get(move))
                    _logger.info(workshop_lines)
                    workshop_lines.write({
                        'move_id': workshop_move.id,
                        'location_dest_id': op_type.default_location_dest_id.id,
                        'picking_id': ws_picking.id
                    })
                ws_picking.action_assign()
                workshop_picking |= ws_picking
        return workshop_picking

    def run_quality_test(self):
        q_test_id = self.env['ir.config_parameter'].sudo().get_param('mobile_device_reception.quality_test_op_type')
        if int(q_test_id) == self.picking_type_id.id:
            return {
                'name': 'Run Quality Test',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'mobile.quality.test.wizard',
                'view_id': False,
                'target': 'new',
            }
