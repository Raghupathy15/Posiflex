# -*- coding: utf-8 -*-

from datetime import date, datetime
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError, UserError, ValidationError

class Tickets(models.Model):
	_name = 'tickets'
	_inherit = 'mail.thread'
	_description = 'Tickets'

	def compute_count(self):
		for record in self:
			record.quotation_count = self.env['sale.order'].search_count([('service_id', '=', self.id)])

	name = fields.Char(string="Name",default="New", readonly=True, track_visibility='always')
	contact = fields.Integer(string='Contact No',readonly=True)
	email = fields.Char(string='Email',readonly=True)
	date_creation = fields.Date('Created Date', readonly=True, default=fields.Date.today())
	service_date = fields.Date('Approx Service Date')
	service_category = fields.Selection([('repair','Repair'),('replacement','Replacement'),('maintanance','Maintanance')],
						string="Service Category",track_visibility='onchange',required=True,default='repair')
	state = fields.Selection([('open', 'Open'), ('assigned', 'Assigned'),('in_progress', 'In Progress'),
		('closed', 'Closed'),('reject', 'Rejected')],string="State", track_visibility='onchange', default="open")
	remarks = fields.Text(string='Remarks')
	rej_remarks = fields.Text(string='Rej Remarks',track_visibility='always')
	quotation_count = fields.Integer('Quotations',compute='compute_count')
	is_quote_created = fields.Boolean('Quotations')
	# Relational fields
	customer_id = fields.Many2one('res.partner',string='Customer',required=True)
	assign_id = fields.Many2one('hr.employee',string='Assign to',required=True)
	product_ids = fields.One2many('service.products','header_id',string='Product Details')
	attachment_ids = fields.One2many('attachment','header_id',string='Attachments')
	activity_ids = fields.One2many('ticket.activity','header_id',string='Activities')
	company_id = fields.Many2one('res.company','Company',index=True, default=lambda self: self.env.company)
	sale_ids = fields.One2many('sale.order', 'service_id', string="Sale")

	@api.model
	def create(self,vals):
		vals['name'] = self.env['ir.sequence'].next_by_code('tickets') or _('New')
		return super(Tickets, self).create(vals)

	@api.onchange('customer_id')
	def onchange_customer_id(self):
		for rec in self:
			if rec.customer_id:
				rec.contact = rec.customer_id.mobile
				rec.email = rec.customer_id.email

	def get_quotation(self):
		self.ensure_one()
		return {
			'type': 'ir.actions.act_window',
			'name': 'Quotation',
			'view_mode': 'tree,form',
			'res_model': 'sale.order',
			'domain': [('service_id', '=', self.id)],
			'context': "{'create': False}"
		}

	def button_quotation(self):
		action = self.env.ref("sale_crm.sale_action_quotations_new").read()[0]
		sale_order = self.env['sale.order']
		sale_order_line = self.env['sale.order.line']
		sale_obj = sale_order.create({
				   'partner_id':self.customer_id.id,
				   'service_id':self.id,
				   })
		sale_line_obj = sale_order_line.create({
				   'product_id':41,
				   'order_id':sale_obj.id,
				   })
		self.write({'is_quote_created':True})

	def button_submit(self):
		self.write({'state':'assigned'})

	def button_in_progress(self):
		self.write({'state':'in_progress'})

	def button_close(self):
		self.write({'state':'closed'})

	def button_reject(self):
		form_view = self.env.ref('indglobal_service.reject_details_view_id')
		return {
				'name': "Reject Remarks",
				'view_mode': 'form',
				'view_type': 'form',
				'view_id': form_view.id,
				'res_model': 'ticket.reject.remark',
				'type': 'ir.actions.act_window',
				'target': 'new',
			}

class ServiceProducts(models.Model):
	_name = 'service.products'
	_description = "Product Details"

	product_id = fields.Many2one('product.product', 'Product Name',required=True)
	categ_id = fields.Many2one('product.category', 'Product category',readonly=True)
	product_uom_qty = fields.Float('Quantity')
	header_id = fields.Many2one('tickets')

	@api.constrains('product_id')
	def _check_exist_product_id(self):
		exist_product_list = []
		for prod in self:
			if prod.product_id.id in exist_product_list:
				raise ValidationError(_('Product should be unique.'))
			exist_product_list.append(prod.product_id.id)

	@api.constrains('product_uom_qty')
	def _check_product_uom_qty(self):
		for product in self:
			if product.product_uom_qty < 1:
				raise UserError('Product Qty should be greater than Zero !!!')

	@api.onchange('product_id')
	def onchange_product_id(self):
		for rec in self:
			if rec.product_id:
				rec.categ_id = rec.product_id.categ_id.id

class Attachment(models.Model):
	_name = 'attachment'
	_description = "Attachment"

	name = fields.Char('Description')
	user_id = fields.Many2one('res.users',string='Attached By',default=lambda self:self.env.user,readonly=True)
	date = fields.Date('Date',default=fields.Date.context_today,readonly=True)
	existing=fields.Binary("Attachment")
	attachment=fields.Char("Attachment")
	header_id = fields.Many2one('tickets')

class TicketActivity(models.Model):
	_name = 'ticket.activity'
	_description = "Ticket Activities"

	name = fields.Char('Description')
	user_id = fields.Many2one('res.users',string='Attached By',default=lambda self:self.env.user,readonly=True)
	activity_id = fields.Many2one('mail.activity.type',string='Activity')
	date = fields.Date('Date',default=fields.Date.context_today,readonly=True)
	header_id = fields.Many2one('tickets')
