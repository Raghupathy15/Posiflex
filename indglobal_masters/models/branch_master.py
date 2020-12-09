# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models,_
import re
from odoo.exceptions import ValidationError,UserError

class Branch(models.Model):
	_name = "branch.master"
	_description = "Branch master"
	_inherit = 'mail.thread'

	name = fields.Char(string='Branch Name',required=True,track_visibility='always')
	partner_id = fields.Many2one('hr.employee','Service Executive/Partner', track_visibility='always',domain="[('user_level', '=','partner')]")