# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Leave
class HRLeave(surya.Sarpam):
    _name = "hr.leave"

    date = fields.Date(string="Date")
    month_id = fields.Many2one(comodel_name="month.attendance", string="Month")
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    leave_level_id = fields.Many2one(comodel_name="leave.level",
                                     string="Leave Level",
                                     related="employee_id.leave_level_id")

    leave_type_id = fields.Many2one(comodel_name="leave.type", string="Leave Type")
    debit = fields.Float(string="Leave Debit")
    credit = fields.Float(string="Leave Credit")
    partial_reconcile_id = fields.Many2one(comodel_name="hr.leave", string="Partial Reconcile")
    reconcile_id = fields.Many2one(comodel_name="hr.leave", string="Reconcile")
    leave_order = fields.Integer(string="Order Sequence")









