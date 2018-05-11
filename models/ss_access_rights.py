# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from datetime import datetime
import json


class SSAccessRights(models.Model):
    _name = 'ss.access.rights'

    name = fields.Char(string='Name')
    access = fields.Text(string='Access')

