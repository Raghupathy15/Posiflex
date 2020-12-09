# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models,_
import re
from odoo.exceptions import ValidationError,UserError

class ZoneMaster(models.Model):
	_name = "zone.master"
	_description = "Zone master"
	_inherit = 'mail.thread'

	name = fields.Char(string='Zone Name')