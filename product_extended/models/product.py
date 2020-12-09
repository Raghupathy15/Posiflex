# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError, UserError, ValidationError

class ProductTemplate(models.Model):
	_inherit = 'product.template'	

	model_no = fields.Char(string="Model No")
	manufacturer_part = fields.Char(string="Manufacturer Part")
	base_uom = fields.Many2one('uom.uom', string="Base UOM")
	inventory_posting_group = fields.Char(string="Inventory Posting Group")
	unit_price = fields.Float(string="Unit Price")
	profit_calc = fields.Float(string="Profit Calc")
	prevent_negative_invent = fields.Char(string="Prevent Negative Inventory")
	bis = fields.Char(string="Bis")
	bis_start_date = fields.Date(default=fields.Date.context_today, string="Bis Start Date")
	bis_exp_date = fields.Date(default=fields.Date.context_today, string="Bis Expiry Date")
	buyer_group = fields.Char(string="Buyer Group")
	item_tracking = fields.Char(string="Item Tracking")
	item_group = fields.Char(string="Item Group")
	length = fields.Float(string="Length (MM)")
	width = fields.Float(string="Width (MM)")
	height = fields.Float(string="Height (MM)")
	description = fields.Char(string="Description")
	cpu = fields.Char(string="CPU")
	memory = fields.Char(string="Memory")
	storage = fields.Char(string="Storage")
	display = fields.Char(string="Display")
	touch = fields.Char(string="Touch")
	os = fields.Char(string="OS")
	interface = fields.Char(string="Interface")
	network = fields.Char(string="Network")
	scanner = fields.Char(string="Scanner")
	warranty_period = fields.Char(string="Warranty Months")