# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models,_
import re
from odoo.exceptions import ValidationError,UserError

class CustomerGroups(models.Model):
	_name = "customer.groups"
	_description = "Customer Groups"
	_inherit = 'mail.thread'

	name = fields.Char('Name',track_visibility='always')