# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


class Address(surya.Sarpam):
    _name = "hospital.address"
    _inherit = "mail.thread"

    door_no = fields.Char(string="Door No")
    building_name = fields.Char(string="Building Name")
    street_1 = fields.Char(string="Street 1")
    street_2 = fields.Char(string="Street 2")
    locality = fields.Char(string="locality")
    landmark = fields.Char(string="landmark")
    city = fields.Char(string="City")
    state_id = fields.Many2one(comodel_name="hospital.state", string="State")
    country_id = fields.Many2one(comodel_name="res.country", string="Country")
    pin_code = fields.Char(string="Pincode")
