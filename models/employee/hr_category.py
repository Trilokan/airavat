# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


# Category
class HRCategory(surya.Sarpam):
    _name = "hr.category"

    name = fields.Char(string="Category", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["progress"] = "confirmed"
        vals["writter"] = "Employee Category Created by {0}".format(self.env.user.name)
        return vals