# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Account Information
class HRAccountInfo(surya.Sarpam):
    _name = "hr.account.info"

    bank = fields.Char(string="Bank", required=True)
    account_no = fields.Char(string="Account No")
    aadhar_card = fields.Char(string="Aadhar Card")
    pan_card = fields.Char(string="Pan Card")
    driving_license = fields.Char(string="Driving License")
    passport = fields.Char(string="Passport")
    epf_no = fields.Char(string="EPF No")
    epf_nominee = fields.Char(string="EPF Nominee")
