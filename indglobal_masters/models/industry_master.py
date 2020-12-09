# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models,_
import re
from odoo.exceptions import ValidationError,UserError

class Industry(models.Model):
	_name = "industry.master"
	_description = "Industry master"
	_inherit = 'mail.thread'

	name = fields.Char(string='Industry Name',required=True,track_visibility='always')