# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from datetime import datetime
import json


class Sarpam(models.Model):
    _name = 'sarpam.sarpam'

    active = fields.Boolean(string='Active', default=True)
    record_comment = fields.Html(string='Record Comment', readonly=True)
    access = fields.Text(string="Access", readonly=True)
    progress = fields.Selection(selection=[], string='Selection')

    def default_vals_creation(self, vals):
        return vals

    def default_rec_creation(self, rec):
        pass

    def record_rights(self):
        pass

    def create_condition_check(self):
        pass

    def check_progress_rights(self):
        self.group_rights()
        self.record_rights()

    def group_rights(self):
        message = 'You need authorisation rigths to do this '

        access_obj = self.env['ss.access.rights'].search([('name', '=', self._name)])

        if access_obj:
            # raise exceptions.ValidationError(message)

            access = json.loads(access_obj.access)
            group_list = access[str(self.progress)]

            group_ids = self.env.user.groups_id
            status = False
            for group in group_ids:
                if group.name in group_list:
                    status = True

            if not status:
                raise exceptions.ValidationError(message)

    @api.multi
    def unlink(self):
        self.check_progress_rights()
        return super(Sarpam, self).unlink()

    @api.multi
    def write(self, vals):
        self.check_progress_rights()
        return super(Sarpam, self).write(vals)

    @api.model
    def create(self, vals):
        self.check_progress_rights()
        self.create_condition_check()
        vals = self.default_vals_creation(vals)
        rec = super(Sarpam, self).create(vals)
        self.default_rec_creation(rec)
        return rec

