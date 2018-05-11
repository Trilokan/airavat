# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class HospitalLocation(surya.Sarpam):
    _name = "hospital.location"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    progress = fields.Selection(selection=PROGRESS_INFO, string="progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    _sql_constraints = [('unique_code', 'unique (code)', 'Error! Group Code must be unique'),
                        ('unique_name', 'unique (name)', 'Error! Group must be unique')]

    def default_vals_creation(self, vals):
        vals["progress"] = "confirmed"
        vals["writter"] = "Product Location Created by {0}".format(self.env.user.name)
        return vals
