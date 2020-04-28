# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class Picking(models.Model):
    _inherit = "stock.picking"

    functional_test_done = fields.Boolean(string='All Quality Test Done', compute='_check_functional_test')
    esthetic_test_done = fields.Boolean(string='All Quality Test Done', compute='_check_esthetic_test')

    show_f_test = fields.Boolean(compute="_check_f_test")
    show_e_test = fields.Boolean(compute="_check_e_test")

    def _check_f_test(self):
        f_test_id = self.env['ir.config_parameter'].sudo().get_param('quality_mobile_test.functional_test_op_type')
        for picking in self:
            if f_test_id:
                if int(f_test_id) == picking.picking_type_id.id:  # picking.company_id.functional_test_op_type
                    picking.show_f_test = True
                else:
                    picking.show_f_test = False
            else:
                picking.show_f_test = False

    def _check_e_test(self):
        e_test_id = self.env['ir.config_parameter'].sudo().get_param('quality_mobile_test.esthetic_test_op_type')
        for picking in self:
            if e_test_id:
                if int(e_test_id) == picking.picking_type_id.id:  # picking.company_id.esthetic_test_op_type
                    picking.show_e_test = True
                else:
                    picking.show_e_test = False
            else:
                picking.show_e_test = False

    def _check_functional_test(self):
        for picking in self:
            test_done = True
            for move in picking.move_line_ids:
                if not move.functional_test_done:
                    test_done = False
            picking.functional_test_done = test_done

    def _check_esthetic_test(self):
        for picking in self:
            test_done = True
            for move in picking.move_line_ids:
                if not move.esthetic_test_done:
                    test_done = False
            picking.esthetic_test_done = test_done

    def button_validate(self):
        f_test_id = int(self.env['ir.config_parameter'].sudo().get_param('quality_mobile_test.functional_test_op_type'))
        e_test_id = int(self.env['ir.config_parameter'].sudo().get_param('quality_mobile_test.esthetic_test_op_type'))
        if self.picking_type_id.id == f_test_id:
            if not self.functional_test_done:
                raise ValidationError("You must run functional test in all lots to validate this stock move.")
            else:
                return super(Picking, self).button_validate()
        elif self.picking_type_id.id == e_test_id:
            if not self.esthetic_test_done:
                raise ValidationError("You must run esthetic test in all lots to validate this stock move.")
            else:
                # First check if there is move lines to SAT location.
                move_to_workshop = self._check_workshop_lines()
                if move_to_workshop:
                    self._create_workshop_move()
                    # raise ValidationError("There is lines to move to SAT")
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
        workshop_op_type = int(self.env['ir.config_parameter'].sudo().get_param('quality_mobile_test.workshop_op_type'))
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
                    if move_line.move_id.id in move_map.keys():
                        move_map.update({move_line.move_id.id: move_map.get(move_line.move_id.id).append(move_line.id)})
                    else:
                        move_map[move_line.move_id.id] = [move_line.id]
                for move in move_map:
                    picking_move = picking.move_lines.filtered(lambda m: m.id == move)
                    workshop_move_id = picking_move._split(len(move_map.get(move)))
                    workshop_move = self.env['stock.move'].search([('id', '=', workshop_move_id)])
                    workshop_move.write({
                        'picking_id': ws_picking.id,
                        'location_dest_id': ws_picking.location_dest_id.id,
                        'state': 'assigned'
                    })

                    # workshop_move = picking_move.copy({
                    #     'move_line_ids': [],
                    #     'picking_id': ws_picking.id,
                    #     'location_id': ws_picking.location_id.id,
                    #     'location_dest_id': ws_picking.location_dest_id.id,
                    #     'product_uom_qty': len(move_map.get(move))
                    # })
                    # picking_move.write({
                    #     # 'product_qty': picking_move.product_qty - len(move_map.get(move)),
                    #     'product_uom_qty': picking_move.product_uom_qty - len(move_map.get(move)),
                    # })
                    workshop_lines = move_lines_to_workshop.filtered(lambda m: m.id in move_map.get(move))
                    workshop_lines.write({
                        'move_id': workshop_move.id,
                        'location_dest_id': op_type.default_location_dest_id.id,
                        'picking_id': ws_picking.id
                    })
                ws_picking.action_assign()
                workshop_picking |= ws_picking
        return workshop_picking

    def run_esthetic_test(self):
        e_test_id = self.env['ir.config_parameter'].sudo().get_param('quality_mobile_test.esthetic_test_op_type')
        if int(e_test_id) == self.picking_type_id.id:
            return {
                'name': 'Run Esthetic Test',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'mobile.esthetic.test.wizard',
                # 'res_id': res_id,
                'view_id': False,
                'target': 'new',
            }
        else:
            msg = self.env['message.popup']
            return msg.popup(message='This must run only in picking type %s' % self.company_id.esthetic_test_op_type)

    def run_functional_test(self):
        f_test_id = self.env['ir.config_parameter'].sudo().get_param('quality_mobile_test.functional_test_op_type')
        if int(f_test_id) == self.picking_type_id.id:
            return {
                'name': 'Run Functional Test',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'mobile.functional.test.wizard',
                # 'res_id': res_id,
                'view_id': False,
                'target': 'new',
            }
        else:
            msg = self.env['message.popup']
            return msg.popup(message='This must run only in picking type %s' % self.company_id.functional_test_op_type)
