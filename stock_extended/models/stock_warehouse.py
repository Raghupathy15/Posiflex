# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError, UserError, ValidationError

class StockWarehouse(models.Model):
	_inherit = 'stock.warehouse'

	warehouse_type = fields.Char(string="Type")
	state = fields.Char(string="State")

class StockLocation(models.Model):
	_inherit = 'stock.location'

	interim_account = fields.Integer(string="Interim account")
	goods_transit = fields.Integer(string="Goods in Transit Account")
	ecc_number = fields.Char(string="ECC Number")
	lst_number = fields.Char(string="LST Number")
	cst_number = fields.Char(string="CST Number")
	service_tax = fields.Char(string="Service Tax Reg No")
	