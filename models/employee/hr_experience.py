# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Experience
class HRExperience(surya.Sarpam):
    _name = "hr.experience"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    name = fields.Char(string="Name", required=True)
    position = fields.Char(string="Position", required=True)
    total_years = fields.Float(string="Total Years", required=True)
    relieving_reason = fields.Text(string="Relieving Reason", required=True)
