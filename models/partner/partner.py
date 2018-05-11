# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

# Partner
PROGRESS_INFO = [("draft", "Draft"),
                 ("confirmed", "Confirmed")]


class HospitalPartner(surya.Sarpam):
    _name = "hospital.partner"
    _inherit = ["hospital.address", "mail.thread"]

    date = fields.Date(string="Date", readonly=True)
    name = fields.Char(string="Name", required=True)
    partner_uid = fields.Char(string="Partner UID", readonly=True)
    image = fields.Binary(string="Image")
    small_image = fields.Binary(string="Image")
    progress = fields.Selection(selection=PROGRESS_INFO, string='Progress', default='draft')

    is_company = fields.Boolean(string="Is Company")
    is_user = fields.Boolean(string="Is User")
    is_employee = fields.Boolean(string="Is Employee")
    is_supplier = fields.Boolean(string="Is Supplier")
    is_patient = fields.Boolean(string="Is Patient")
    is_service = fields.Boolean(string="Is Service")

    gst_no = fields.Char(string="GST No")
    license_no = fields.Char(string="License No")
    tin_no = fields.Char(string="TIN No")
    pan_no = fields.Char(string="PAN No")

    contact_person = fields.Char(sring="Contact Person")
    email = fields.Char(string="Email")
    mobile = fields.Char(string="Mobile", required=True)
    alternate_contact = fields.Char(string="Alternate Contact")

    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):

        vals["partner_uid"] = self.env['ir.sequence'].next_by_code(self._name)
        vals["date"] = datetime.now().strftime("%Y-%m-%d")
        vals["progress"] = "confirmed"
        vals["writter"] = "Partner record created by {0}".format(self.env.user.name)

        return vals


