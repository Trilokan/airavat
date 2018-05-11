# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


# Department
class HRDepartment(surya.Sarpam):
    _name = "hr.department"

    name = fields.Char(string="Department", required=True)
    head_id = fields.Many2one(comodel_name="hr.employee", string="Department Head")
    member_ids = fields.Many2many(comodel_name="hr.employee", string="Department Members")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["progress"] = "confirmed"
        vals["writter"] = "Department Created by {0}".format(self.env.user.name)
        return vals
