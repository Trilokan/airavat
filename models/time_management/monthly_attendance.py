# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime, timedelta
from .. import surya
from lxml import etree


# Week Schedule

PROGRESS_INFO = [('draft', 'draft'), ('open', 'Open'), ('verified', 'verified')]


class MonthAttendance(surya.Sarpam):
    _name = "month.attendance"
    _rec_name = "period_id"

    period_id = fields.Many2one(comodel_name="period.period", string="Month")
    month_detail = fields.One2many(comodel_name="time.attendance",
                                   inverse_name="month_id",
                                   string="Month Detail")
    progress = fields.Selection(PROGRESS_INFO, string='Progress', default="draft")

    def calc_total_days(self):
        from_date = datetime.strptime(self.period_id.from_date, "%Y-%m-%d")
        till_date = datetime.strptime(self.period_id.till_date, "%Y-%m-%d")

        return (till_date - from_date).days

    def calc_total_present(self, employee):
        full_day = self.env["time.attendance.detail"].search_count([("employee_id", "=", employee.id),
                                                                    ("attendance_id.month_id", "=", self.id),
                                                                    ("availability_progress", "=", "full_day")])
        half_day = self.env["time.attendance.detail"].search_count([("employee_id", "=", employee.id),
                                                                    ("attendance_id.month_id", "=", self.id),
                                                                    ("availability_progress", "=", "half_day")])

        return full_day + (0.5 * half_day)

    def calc_total_absent(self, employee):
        absent = self.env["time.attendance.detail"].search_count([("employee_id", "=", employee.id),
                                                                  ("attendance_id.month_id", "=", self.id),
                                                                  ("day_progress", "=", "working_day"),
                                                                  ("availability_progress", "=", "absent")])

        return absent

    def calc_total_working_days(self, employee):
        working_days = self.env["time.attendance.detail"].search_count([("employee_id", "=", employee.id),
                                                                        ("attendance_id.month_id", "=", self.id),
                                                                        ("day_progress", "=", "working_day")])

        return working_days

    def calc_total_holidays(self, employee):
        holidays = self.env["time.attendance.detail"].search_count([("employee_id", "=", employee.id),
                                                                    ("attendance_id.month_id", "=", self.id),
                                                                    ("day_progress", "=", "holiday")])

        return holidays

    @api.multi
    def trigger_closed(self):
        draft = self.env["time.attendance"].search_count([("month_id", "=", self.id), ("progress", "!=", "verified")])

        if draft:
            raise exceptions.ValidationError("Error! Daily attendance report is not verified")

        employees = self.env["hr.employee"].search([])
        for employee in employees:
            total_days = self.calc_total_days()
            total_present = self.calc_total_present(employee)
            total_absent = self.calc_total_absent(employee)
            total_working_days = self.calc_total_working_days(employee)
            total_holidays = self.calc_total_holidays(employee)

            hr_leave = {"employee_id": employee.id,
                        "month_id": self.id,
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "debit": (total_holidays + total_working_days) - (total_present + total_absent)}
            self.env["hr.leave"].create(hr_leave)

        self.write({"progress": "verified"})

    @api.multi
    def trigger_open(self):
        configs = self.env["leave.configuration"].search([])

        for config in configs:
            employees = self.env["hr.employee"].search([('leave_level_id', '=', config.leave_level_id.id)])

            for employee in employees:
                hr_leave = {"employee_id": employee.id,
                            "month_id": self.id,
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "leave_type_id": config.leave_type_id.id,
                            "credit": config.leave_credit,
                            "leave_order": config.leave_order}

                self.env["hr.leave"].create(hr_leave)

        self.write({"progress": "open"})

    def get_opening_leave(self, month, employee):
        opening = 0
        opening_recs = self.env["hr.leave"].search([("employee_id", "=", employee.id),
                                                    ("month_id", "=", month.id),
                                                    ("credit", ">", 0)])

        for rec in opening_recs:
            opening = opening + rec.credit

        return opening

    def get_credit_debit_leave(self, month, employee):
        credits = debits = lop = 0

        credit_recs = self.env["hr.leave"].search([("employee_id", "=", employee.id),
                                                   ("month_id", "=", month.id),
                                                   ("credit", ">", 0)])
        for rec in credit_recs:
            credits = credits + rec.credit

        debit_recs = self.env["hr.leave"].search([("employee_id", "=", employee.id),
                                                  ("month_id", "=", month.id),
                                                  ("debit", ">", 0)])

        for rec in debit_recs:
            debits = debits + rec.debit

        return credits, debits

    @api.multi
    def trigger_lop_calculation(self, months, employee):
        opening = total_credits = total_debits = lop = 0

        if months:
            opening = self.get_opening_leave(months[0], employee)

        for month in months:
            credit, debit = self.get_credit_debit_leave(month, employee)
            total_credits = total_credits + credit
            total_debits = total_debits + debit

            if total_debits > total_credits:
                lop = total_debits - total_credits
                total_credits = total_credits + lop

            closing = total_credits - total_debits

            return opening, credit, debit, lop, closing

    @api.multi
    def trigger_leave_opening_closing_report(self):
        employees = self.env["hr.employee"].search([])

        for employee in employees:
            months = self.env["month.attendance"].search([])

            opening, credit, debit, lop, closing = self.trigger_lop_calculation(months, employee)

    @api.multi
    def trigger_monthly_attendance_report(self):
        pass
