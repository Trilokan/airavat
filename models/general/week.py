# -*- coding: utf-8 -GPK*-

from odoo import fields, api, exceptions
from .. import surya

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class Week(surya.Sarpam):
    _name = "week.week"
    _rec_name = "name"
    _inherit = "mail.thread"

    name = fields.Char(string="Week", required=True)
    year_id = fields.Many2one(comodel_name="year.year", string="Year")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["progress"] = "confirmed"
        vals["writter"] = "State Created by {0}".format(self.env.user.name)
        return vals
