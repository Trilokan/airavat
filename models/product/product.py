# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json


# Product Group
PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]
PRODUCT_TYPE = [("service", "Service"), ("medicine", "Medicine")]


class Product(surya.Sarpam):
    _name = "hospital.product"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", readonly=True)
    group_id = fields.Many2one(comodel_name="product.group", string="Group", required=True)
    sub_group_id = fields.Many2one(comodel_name="product.sub.group", string="Sub Group", required=True)
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", required=True)
    product_type = fields.Selection(selection=PRODUCT_TYPE, string="Product Type", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="progress", default="draft")
    comment = fields.Text(string="Comment")
    warehouse_ids = fields.One2many(comodel_name="hospital.warehouse",
                                    inverse_name="product_id",
                                    string="Warehouse",
                                    domain=lambda self: [('location_id', '!=', self.env.user.company_id.virtual_location_id.id)],
                                    readonly=True)

    min_stock = fields.Integer(string="Min Stock")
    max_stock = fields.Integer(string="Max Stock")
    writter = fields.Text(string="Writter", track_visibility="always")

    _sql_constraints = [('unique_code', 'unique (code)', 'Error! Product Code must be unique'),
                        ('unique_name', 'unique (name)', 'Error! Product must be unique')]

    def default_vals_creation(self, vals):
        group_id = self.env["product.group"].search([("id", "=", vals["group_id"])])
        sub_group_id = self.env["product.group"].search([("id", "=", vals["sub_group_id"])])
        code = "{0}/{1}/{2}".format(group_id.code,
                                    sub_group_id.code,
                                    self.env["ir.sequence"].next_by_code(self._name))
        vals["code"] = code
        vals["progress"] = "confirmed"
        vals["writter"] = "Product Created by {0}".format(self.env.user.name)
        return vals

    def default_rec_creation(self, rec):
        location_id = self.env.user.company_id.location_id
        self.env["hospital.warehouse"].create({"product_id": rec.id,
                                               "location_id": location_id.id,
                                               "progress": "confirmed"})

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search(['|', ('name', '=', name), ('code', '=', name)] + args, limit=limit)
        if not recs:
            recs = self.search(['|', ('name', operator, name), ('code', operator, name)] + args, limit=limit)
        return recs.name_get()

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "[{0}] {1}".format(record.code, record.name)
            result.append((record.id, name))
        return result


