# -*- coding: utf-8 -GPK*-

from odoo import fields, api, exceptions
from .. import surya

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class Year(surya.Sarpam):
    _name = "year.year"
    _rec_name = "name"
    _inherit = "mail.thread"

    name = fields.Char(string="Year", required=True)
    financial_year = fields.Char(string="Financial Year", required=True)
    period_detail = fields.One2many(comodel_name="period.period",
                                    inverse_name="year_id",
                                    string="Period",
                                    readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["progress"] = "confirmed"
        vals["writter"] = "State Created by {0}".format(self.env.user.name)
        return vals
