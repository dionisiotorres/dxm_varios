# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class EstheticQualityTest(models.Model):
    _name = 'esthetic.quality.test'
    _description = 'Product Visual Tests'

    move_ids = fields.Many2many(comodel_name='stock.move.line')  # inverse_name='functional_test_id'
    lot_id = fields.Char(string="Find Lot")

    test_result = fields.Char(string="Test Result")

    def _get_grade_display_questions(self):
        display_selection = []
        grades = self.env['x_grado'].search([('x_studio_is_grade_test', '=', True)])
        for grade in grades:
            display_selection.append((str(grade.x_studio_test_value),  grade.x_studio_display_short_description))
        return display_selection

    def _get_grade_case_questions(self):
        case_selection = []
        grades = self.env['x_grado'].search([('x_studio_is_grade_test', '=', True)])
        for grade in grades:
            case_selection.append((str(grade.x_studio_test_value),  grade.x_studio_case_short_description))
        return case_selection

    # Test questions
    display_test = fields.Selection(selection='_get_grade_display_questions', string='Display Status', default='10')
    case_test = fields.Selection(selection='_get_grade_case_questions', string='Case Status', default='10')
    # Accessories Questions
    device_case = fields.Boolean(string='Device Case', default=False)
    charger = fields.Boolean(string='Charger', default=False)
    cables = fields.Boolean(string='Cables', default=False)
    headset = fields.Boolean(string='Headset', default=False)

    def get_esthetic_result(self):
        esthetic_matrix = {}
        grades = self.env['x_grado'].search([('x_studio_is_grade_test', '=', True)])
        for grade in grades:
            esthetic_matrix.update({grade.x_studio_test_value:  grade.x_name})
        _logger.info("Grade Matrix: %r", esthetic_matrix)
        # esthetic_matrix = {'10': 'A', '20': 'B', '30': 'C'}
        display_result = int(self.display_test)
        case_result = int(self.case_test)
        max_value = max(display_result, case_result)
        grade = esthetic_matrix.get(max_value)
        days = all(record for record in [self.device_case, self.charger, self.cables, self.headset])
        if grade == 'A' and days:
            grade = '14 Días'  # todo: get this dynamically
        _logger.info("GRADO: %r", grade)
        return grade

    def name_get(self):
        res = []
        for test in self:
            res.append((test.id, test.get_esthetic_result()))
        return res


class FunctionalQualityTest(models.Model):
    _name = 'functional.quality.test'
    _description = 'Product Visual Tests'

    move_ids = fields.Many2many(comodel_name='stock.move.line')  # inverse_name='functional_test_id'
    lot_id = fields.Char(string="Find Lot")

    test_pass = fields.Boolean(string="Test Pass")

    # Test questions
    power_on = fields.Boolean(string='Power On', default=True)
    speaker = fields.Boolean(string='Speaker', default=True)
    buttons = fields.Boolean(string='Buttons', default=True)
    fingerprint_reader = fields.Boolean(string='Fingerprint Reader', default=True)
    torch = fields.Boolean(string='Torch', default=True)
    bluetooth = fields.Boolean(string='	Bluetooth', default=True)
    wifi = fields.Boolean(string='WiFi', default=True)
    proximity_sensor = fields.Boolean(string='Proximity Sensor', default=True)
    touch_screen = fields.Boolean(string='Touch Screen', default=True)
    display_bright = fields.Boolean(string='Display Bright', default=True)
    call_test = fields.Boolean(string='Call', default=True)
    ring_tone = fields.Boolean(string='Ring Tone', default=True)
    camera = fields.Boolean(string='Camera', default=True)
    mobile_os = fields.Boolean(string='Operating System', default=True)
    user_account = fields.Boolean(string='User Account', default=True)
    security_pattern = fields.Boolean(string='Security Pattern', default=True)
    humidity = fields.Boolean(string='Humidity', default=True)

    def get_functional_result(self):
        """
        Get functional test result
        :return: True or False
        """
        _logger.info("GETTING TEST RESULT FOR: %r", self.id)
        exclude_fields = ['id', 'display_name', 'create_uid', 'create_date', 'write_uid', 'write_date',
                          '__last_update', 'test_pass', 'move_ids', 'lot_id']
        fields_to_read = [element for element in self.fields_get_keys() if element not in exclude_fields]
        values = self.read(fields_to_read)[0].values()
        _logger.info(values)
        return all(record for record in values)

    def name_get(self):
        res = []
        for test in self:
            if test.test_pass:
                res.append((test.id, "Sin Avería"))
            else:
                res.append((test.id, "Con Avería"))
        return res
