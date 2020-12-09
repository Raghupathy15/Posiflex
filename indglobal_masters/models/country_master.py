# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models,_
import re
from odoo.exceptions import ValidationError,UserError

class Country(models.Model):
	_description = "Country state"
	_inherit = "res.country"

	code_tds = fields.Char('Country Code for eTDS/TCS')
	intrastat_code = fields.Char('Intrastat Code')