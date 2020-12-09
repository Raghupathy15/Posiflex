import base64
import os
import re
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError

class Users(models.Model):
	_inherit = "res.users"

	sales_manager_id = fields.Many2one('hr.employee',string='Sales Manager')
	rsm_id = fields.Many2one('hr.employee', 'RSM')
	sales_head_id = fields.Many2one('hr.employee', 'Sales Head')