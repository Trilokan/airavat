# -*- coding: utf-8 -GPK*-

from odoo import fields, api, exceptions
from .. import surya
from datetime import datetime, timedelta

PROGRESS_INFO = [("draft", "Draft"), ("open", "Open"), ("closed", "Closed")]


class Period(surya.Sarpam):
    _name = "period.period"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", readonly=True)
    year_id = fields.Many2one(comodel_name="year.year", string="Year", readonly=True)
    from_date = fields.Date(string="From Date", required=True)
    till_date = fields.Date(string="Till Date", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    @api.multi
    def trigger_period_open(self):
        self.check_progress([("progress", "=", "open")])
        writter = "Period Open by {0}".format(self.env.user.name)
        self.write({"progress": "open", "writter": writter})

    @api.multi
    def trigger_period_closed(self):
        self.check_progress([("progress", "=", "open"), ("id", "!=", self.id)])
        writter = "Period Open by {0}".format(self.env.user.name)
        self.write({"progress": "closed", "writter": writter})

    def check_progress(self, data):
        if self.env["period.period"].search(data):
            raise exceptions.ValidationError("Error! Please close the existing period before open new period")

    def default_vals_creation(self, vals):
        from_date = datetime.strptime(vals["from_date"], "%Y-%m-%d")
        till_date = datetime.strptime(vals["till_date"], "%Y-%m-%d")

        last_from_date = from_date - timedelta(days=1)
        next_till_date = till_date + timedelta(days=1)

        # Check period within a month
        if from_date.strftime("%m-%Y") != till_date.strftime("%m-%Y"):
            raise exceptions.ValidationError("Error! Period must be within a month")

        if last_from_date.strftime("%m-%Y") == till_date.strftime("%m-%Y"):
            raise exceptions.ValidationError("Error! Period must be within a month")

        if from_date.strftime("%m-%Y") == next_till_date.strftime("%m-%Y"):
            raise exceptions.ValidationError("Error! Period must be within a month")

        vals["name"] = "{0} To {1}".format(from_date.strftime("%d-%m-%Y"), till_date.strftime("%d-%m-%Y"))

        year = self.env["year.year"].search([("name", "=", from_date.strftime("%Y"))])
        if year:
            vals["year_id"] = year.id
        else:
            raise exceptions.ValidationError("Error! Please create year before period creation")

        return vals



