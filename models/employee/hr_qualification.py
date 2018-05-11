# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

RESULT_INFO = [('pass', 'Pass'), ('fail', 'Fail'), ('discontinued', 'Discontinued')]


# Qualification
class HRQualification(surya.Sarpam):
    _name = "hr.qualification"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    name = fields.Char(string="Name", required=True)
    institution = fields.Char(string="Institution", required=True)
    result = fields.Selection(selection=RESULT_INFO, string='Pass/Fail', required=True)
    enrollment_year = fields.Integer(string="Enrollment Year", required=True)
    completed_year = fields.Integer(string="Completed Year")
