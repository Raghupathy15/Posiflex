# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models,_
import re
from odoo.exceptions import ValidationError,UserError

class CountryState(models.Model):
	_description = "Country state"
	_inherit = "res.country.state"

	code_tds = fields.Char('State Code for eTDS/TCS')
	tin_code = fields.Char('State Code for TIN')