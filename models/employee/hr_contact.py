# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Contacts

class HRContact(surya.Sarpam):
    _name = "hr.contact"
    _inherit = "hospital.address"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
