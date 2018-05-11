# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class Employee(surya.Sarpam):
    _name = "hr.employee"
    _inherit = ["hr.account.info", "hr.personal.info", "hospital.address"]

    date = fields.Date(string="Date", readonly=True)
    name = fields.Char(string="Name", required=True)
    employee_uid = fields.Char(string="Employee ID", readonly=True)
    image = fields.Binary(string="Image")
    small_image = fields.Binary(string="Image")
    progress = fields.Selection(selection=PROGRESS_INFO, string='Progress', default='draft')

    # Contact
    email = fields.Char(string="Email")
    mobile = fields.Char(string="Mobile", required=True)
    alternate_contact = fields.Char(string="Alternate Contact")

    # HR Details
    doj = fields.Date(string="Date of Joining", required=False)
    date_of_relieving = fields.Date(string="Date of Relieving")
    department_id = fields.Many2one(comodel_name="hr.department", string="Department")
    designation_id = fields.Many2one(comodel_name="hr.designation", string="Designation")
    reporting_to_id = fields.Many2one(comodel_name="hr.employee", string="Reporting To")
    employee_category_id = fields.Many2one(comodel_name="hr.category", string="Employee Category")
    qualification_ids = fields.One2many(comodel_name="hr.qualification",
                                        inverse_name="employee_id",
                                        string="Qualification")
    experience_ids = fields.One2many(comodel_name="hr.experience",
                                     inverse_name="employee_id",
                                     string="Experience")
    leave_ids = fields.One2many(comodel_name="hr.leave",
                                inverse_name="employee_id",
                                string="Leave")

    leave_level_id = fields.Many2one(comodel_name="leave.level", string="Leave Level")
    user_id = fields.Many2one(comodel_name="res.users", string="User")

    # Filter Details
    is_doctor = fields.Boolean(string="Doctor")
    is_nurse = fields.Boolean(string="Nurse")
    is_contract = fields.Boolean(string="Contract")
    is_admin_staff = fields.Boolean(string="Admin Staff")
    is_ambulance_driver = fields.Boolean(string="Ambulance Driver")

    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    partner_id = fields.Many2one(comodel_name="hospital.partner", string="Partner")
    writter = fields.Text(string="Writter", track_visibility="always")

    def default_vals_creation(self, vals):
        vals["employee_uid"] = self.env['ir.sequence'].next_by_code(self._name)
        vals["date"] = datetime.now().strftime("%Y-%m-%d")
        vals["progress"] = "confirmed"

        data = {"name": vals["name"],
                "mobile": vals["mobile"],
                "email": vals.get("email", None),
                "alternate_contact": vals.get("alternate_contact", None),
                "is_patient": True}

        partner_id = self.env["hospital.partner"].create(data)
        vals["partner_id"] = partner_id.id
        vals["writter"] = "Employee record created by {0}".format(self.env.user.name)

        return vals
