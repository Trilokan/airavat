# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


BLOOD_GROUP = [('a+', 'A+'), ('b+', 'B+'), ('ab+', 'AB+'), ('o+', 'O+'),
               ('a-', 'A-'), ('b-', 'B-'), ('ab-', 'AB-'), ('o-', 'O-')]
GENDER = [('male', 'Male'), ('female', 'Female')]
MARITAL_STATUS = [('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced')]


# Personal Information
class HRPersonnelInfo(surya.Sarpam):
    _name = "hr.personal.info"

    age = fields.Integer(string="Age")
    blood_group = fields.Selection(selection=BLOOD_GROUP, string="Blood Group")
    marital_status = fields.Selection(selection=MARITAL_STATUS, string="Marital Status")
    gender = fields.Selection(selection=GENDER, string="Gender")
    caste = fields.Char(string="Caste")
    religion_id = fields.Many2one(comodel_name="res.religion", string="Religion")
    physically_challenged = fields.Boolean(string="Physically Challenged")
    nationality_id = fields.Many2one(comodel_name="res.country")
    mother_toungue_id = fields.Many2one(comodel_name="hospital.language", string="Mother Toungue")
    language_known_ids = fields.Many2many(comodel_name="hospital.language", string="Language Known")
    personnel_mobile = fields.Char(string="Personnel Mobile")
    personnel_email = fields.Char(string="Personnel Email")
    contact_address = fields.Char(string="Contact Address")
    is_contact_differ_permanent = fields.Boolean(string="Is Contact Address From Permanent Address")
    permanent_address = fields.Char(string="Permanent Address")
    family_member_ids = fields.One2many(comodel_name="hr.contact",
                                        inverse_name="employee_id",
                                        string="Family Members")
