# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya

PROGRESS_INFO = [('draft', 'Draft'), ('confirmed', 'Confirmed')]


# Leave Level
class LeaveLevel(surya.Sarpam):
    _name = "leave.level"
    _inherit = "mail.thread"

    name = fields.Char(string="Name")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["progress"] = "confirmed"
        vals["writter"] = "Leave Level Created by {0}".format(self.env.user.name)
        return vals


