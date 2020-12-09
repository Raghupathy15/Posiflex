# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models,_
import re
from odoo.exceptions import ValidationError,UserError

class Company(models.Model):
	_inherit = "res.company"

	telex_no = fields.Char(string='Telex No')
	fax_no = fields.Char(string='FAX No')
	giro_no = fields.Char(string='Giro No')
	bank_name = fields.Char(string='Bank Name')
	bank_acc_no = fields.Char(string='Bank Acc  No')
	bank_branch_no = fields.Char(string='Bank Branch No')
	pmt_routing_no = fields.Char(string='Payment Routing No')
	cus_permit_date = fields.Date(string='Customs Permit Date')
	cus_permit_no = fields.Char(string='Customs Permit No')
	location_code = fields.Char(string='Location code')
	intrastat_contact_no = fields.Char(string='Intrastat Contact No')
	intrastat_contact_type = fields.Selection([('contact', 'Contact'),('vendor','vendor')],string='Ventrastat Contact Type')
	res_center = fields.Char(string='Responsibility Center')
	tin = fields.Char(string='TIN No')
	lst = fields.Char(string='LST No')
	cst = fields.Char(string='CST No')
	pan = fields.Char(string='PAN No')
	ecc = fields.Char(string='ECC No')
	tan = fields.Char(string='TAN No')