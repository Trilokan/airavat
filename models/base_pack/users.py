# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


class HospitalUsers(surya.Sarpam):
    _name = "res.users"
    _inherit = "res.users"

    location_id = fields.Many2one(comodel_name="hospital.location", string="Location")

