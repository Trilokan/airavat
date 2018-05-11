# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Product Sub Group
PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class ProductSubGroup(surya.Sarpam):
    _name = "product.sub.group"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    group_id = fields.Many2one(comodel_name="product.group", string="Group", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, sring="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    _sql_constraints = [('unique_code', 'unique (code)', 'Error! Sub-Group Code must be unique'),
                        ('unique_name', 'unique (name)', 'Error! Sub-Group must be unique')]

    def default_vals_creation(self, vals):
        vals["progress"] = "confirmed"
        vals["writter"] = "Product Sub-Group Created by {0}".format(self.env.user.name)
        return vals
