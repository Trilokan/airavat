# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions, _
from datetime import datetime
from .. import surya
import json

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class HospitalWarehouse(surya.Sarpam):
    _name = "hospital.warehouse"
    _rec_name = "location_id"

    product_id = fields.Many2one(comodel_name="hospital.product", string="Product")
    location_id = fields.Many2one(comodel_name="hospital.location", string="Location")
    quantity = fields.Float(string="Quantity", compute="get_stock")
    progress = fields.Selection(selection=PROGRESS_INFO, string="progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    _sql_constraints = [('unique_product_location', 'unique (product_id, location_id)',
                         'Error! Product location must be unique')]

    def default_vals_creation(self, vals):
        vals["progress"] = "confirmed"
        vals["writter"] = "Product Group Created by {0}".format(self.env.user.name)
        return vals

    @api.multi
    def get_stock(self):
        for record in self:
            destination_ids = self.env["stock.move"].search([("product_id", "=", record.product_id.id),
                                                             ("destination_location_id", "=", record.location_id.id),
                                                             ("progress", "=", "moved")])

            source_ids = self.env["stock.move"].search([("product_id", "=", record.product_id.id),
                                                        ("source_location_id", "=", record.location_id.id),
                                                        ("progress", "=", "moved")])
            quantity_in = quantity_out = 0

            for rec in destination_ids:
                quantity_in = quantity_in + rec.quantity

            for rec in source_ids:
                quantity_out = quantity_out + rec.quantity

            balance = quantity_in - quantity_out
            record.quantity = balance