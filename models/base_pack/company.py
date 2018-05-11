# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


class HospitalCompany(surya.Sarpam):
    _name = "res.company"
    _inherit = "res.company"

    location_id = fields.Many2one(comodel_name="hospital.location", string="Location")
    virtual_location_id = fields.Many2one(comodel_name="hospital.location", string="Virtual Location")
