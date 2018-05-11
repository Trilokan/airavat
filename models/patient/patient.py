# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]
BLOOD_GROUP = [('a+', 'A+'), ('b+', 'B+'), ('ab+', 'AB+'), ('o+', 'O+'),
               ('a-', 'A-'), ('b-', 'B-'), ('ab-', 'AB-'), ('o-', 'O-')]
GENDER = [('male', 'Male'), ('female', 'Female')]
MARITAL_STATUS = [('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced')]


class Patient(surya.Sarpam):
    _name = "hospital.patient"
    _inherit = ["hospital.address", "mail.thread"]

    date = fields.Date(string="Date", readonly=True)
    name = fields.Char(string="Name", required=True)
    patient_uid = fields.Char(string="Patient ID", readonly=True)
    image = fields.Binary(string="Image")
    small_image = fields.Binary(string="Image")
    progress = fields.Selection(selection=PROGRESS_INFO, string='Progress', default='draft')

    # Contact
    email = fields.Char(string="Email", required=True)
    mobile = fields.Char(string="Mobile", required=True)
    alternate_contact = fields.Char(string="Alternate Contact")

    # Professional
    work_position = fields.Char(string="Position")
    work_description = fields.Char(string="Company/Work Details")

    # Personnel Details
    dob = fields.Date(string="Date of Birth")
    gender = fields.Selection(selection=GENDER, string="Gender")
    age = fields.Char(string="Age", compute="_get_age")
    marital_status = fields.Selection(selection=MARITAL_STATUS, string="Marital Status")
    aadhar_no = fields.Char(string="Aadhar No")
    driving_license = fields.Char(string="Driving Licence No")

    # Medical Details
    blood_group = fields.Selection(selection=BLOOD_GROUP, string="Blood Group")
    allergic_towards = fields.Text(string="Allergic Towards")
    # treatment_detail = fields.One2many(comodel_name="hospital.treatment",
    #                                    inverse_name="patient_id",
    #                                    string="Treatment Details")
    report = fields.Html(string="Report")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    partner_id = fields.Many2one(comodel_name="hospital.partner", string="Partner")
    writter = fields.Text(string="Writter", track_visibility="always")

    def _get_age(self):
        for record in self:
            today = datetime.now()
            age_obj = datetime.strptime(record.age, "%Y-%m-%d")
            years = days = 0
            if today > age_obj:
                total_days = (today - age_obj).days
                years = int(total_days/365)
                days = total_days - years*365

            record.age = "({0}) Years ({1}) Days".format(years, days)

    def default_vals_creation(self, vals):

        vals["patient_uid"] = self.env['ir.sequence'].next_by_code(self._name)
        vals["date"] = datetime.now().strftime("%Y-%m-%d")
        vals["progress"] = "confirmed"

        data = {"name": vals["name"],
                "email": vals["email"],
                "mobile": vals["mobile"],
                "alternate_contact": vals.get("alternate_contact",  default=None),
                "is_patient": True}

        partner_id = self.env["hospital.partner"].create(data)
        vals["partner_id"] = partner_id.id
        vals["writter"] = "Patient record created by {0}".format(self.env.user.name)

        return vals

