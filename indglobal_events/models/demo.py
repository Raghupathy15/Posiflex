# -*- coding: utf-8 -*-

from datetime import date, datetime
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError, UserError, ValidationError

class CRMLead(models.Model):
	_inherit = 'crm.lead'
	_description = 'CRM Lead'
	
	def name_get(self):
		result = []
		var = ''
		for line in self:
			name = str(line.contact_name) + var
			result.append((line.id, name))
		return result

class StockPickingEvent(models.Model):
	_inherit = 'stock.picking'
	_description = 'Event Stock Picking'

	demo_id = fields.Many2one('demo.inventory', string="Name")
	from_date = fields.Date(string="From Date", related="demo_id.from_date")
	end_date = fields.Date(string="End Date", related="demo_id.end_date")
	sequence_code = fields.Char(string="Code", related="picking_type_id.sequence_code")

	def action_done(self):
		res = super(StockPickingEvent, self).action_done()
		if self.picking_type_id.sequence_code == 'DOUT':
			for vals in self.demo_id:
				vals.write({'state':'product_sent'})
		elif self.picking_type_id.sequence_code == 'DIN':
			for vals in self.demo_id:
				vals.write({'state':'product_received'})

class StockMoveEvent(models.Model):
	_inherit = 'stock.move'
	_description = 'Event Stock Move'

	sequence_code = fields.Char(string="Code", related="picking_type_id.sequence_code")
	demo_id = fields.Many2one('demo.inventory', string="Name")
	material_condition = fields.Selection([('good', 'Good'),('defect', 'Defect')], string="Material Condition")

class DemoInventory(models.Model):
	_name = 'demo.inventory'
	_description = 'Demo Inventory'
	_inherit = 'mail.thread'
	_order = 'id desc'

	def _get_employee_id(self):
		employee_rec = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
		return employee_rec.id

	name = fields.Char(string="Name", default="New", readonly=True, track_visibility='always')
	purpose = fields.Selection([('demo', 'Demo'),('company_event', 'Company Event'),('partner_event', 'Partner Event'),('testing', 'Testing')], string="Purpose", required=True, track_visibility='onchange')
	demo_period = fields.Selection([('thirty', '30 Days'),('sixty', '60 Days'),('ninty', '90 Days')], string="Demo Period", required=True, track_visibility='onchange')
	employee_id = fields.Many2one('hr.employee', string="Requested by", default=_get_employee_id)
	user_id = fields.Many2one('res.users', string="User", readonly=True, track_visibility='onchange', related="employee_id.user_id")
	request_date = fields.Date(string="Requested Date", readonly=True, default=fields.Datetime.today)
	from_date = fields.Date(string="From Date", track_visibility='onchange', default=fields.Datetime.today)
	end_date = fields.Date(string="End Date", track_visibility='onchange')
	partner_id = fields.Many2one('res.partner', string="Customer", track_visibility='onchange')
	customer_type = fields.Selection([('exist_custom', 'Existing Customer'),('new_custom', 'New Customer')], string="Customer Type")
	new_partner_id = fields.Many2one('crm.lead', string="Customer")
	company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id.id)
	event_catg_id = fields.Many2one('event.category', string="Event Category", track_visibility='onchange')
	state = fields.Selection([('draft', 'Draft'), ('request', 'Request'),('approve', 'Approved'), 
		('reject', 'Rejected'),('product_sent', 'Product Sent'), ('product_received', 'Product Received')],
	 string="State", track_visibility='onchange', default="draft")
	reject_remarks = fields.Text(string="Reject Remarks", track_visibility='onchange', readonly=True)
	product_ids = fields.One2many('product.details', 'demo_id', string="Product Details", required=True)
	specification_ids = fields.One2many('specification.details', 'demo_id', string="Specification")
	picking_ids = fields.One2many('stock.picking', 'demo_id', string="Delivery", compute='_compute_picking_ids')
	move_ids = fields.One2many('stock.move', 'demo_id', string="Stock")
	delivery_count = fields.Integer(string="Delivery Count", compute='_compute_picking_ids')
	specification = fields.Text(string="Specification")
	terms_conditions = fields.Text(string="Terms & Conditions")
	is_rsm = fields.Boolean(string="RSM", compute='_compute_user')
	is_employee = fields.Boolean(string="Is Employee", compute='_compute_user')

	@api.depends('employee_id')
	def _compute_user(self):
		for vals in self:
			if vals.employee_id:
				current_employee = vals.env.uid
				rsm = vals.employee_id.rsm_id.user_id
				if current_employee == rsm.id or vals.env.user._is_admin():
					vals.is_rsm = True
					vals.is_employee = False
				elif current_employee == vals.user_id.id or vals.env.user._is_admin():
					vals.is_rsm = False
					vals.is_employee = True
				else:
					vals.is_rsm = False
					vals.is_employee = False

	@api.depends('name')
	def _compute_picking_ids(self):
		for order in self:
			order.picking_ids = self.env['stock.picking'].search([('demo_id', '=', order.id)])
			order.delivery_count = len(order.picking_ids)

	@api.model
	def create(self,vals):
		vals['name'] = self.env['ir.sequence'].next_by_code('demo.inventory') or _('New')
		return super(DemoInventory, self).create(vals)


	@api.onchange('from_date','demo_period')
	def onchange_validity_days(self):
		if self.from_date and self.demo_period == 'thirty':
			self.end_date = self.from_date + relativedelta(days=30)
		elif self.from_date and self.demo_period == 'sixty':
			self.end_date = self.from_date + relativedelta(days=60)
		elif self.from_date and self.demo_period == 'ninty':
			self.end_date = self.from_date + relativedelta(days=90)

	def action_view_delivery(self):
		""" This function returns an action that display picking related to
		Demo Inventory orders. It can either be a in a list or in a form
		view, if there is only one picking to show.
		"""
		self.ensure_one()
		action = self.env.ref('stock.action_picking_tree_all').read()[0]
		print ('11111111111111',action)
		pickings = self.mapped('picking_ids')
		print ('22222222222222',pickings)
		if len(pickings) > 1:
			action['domain'] = [('id', 'in', pickings.ids)]
		elif pickings:
			form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
			if 'views' in action:
				action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
			else:
				action['views'] = form_view
			action['res_id'] = pickings.id
		return action

	def button_submit(self):
		self.write({'state':'request'})

	def button_draft(self):
		self.write({'state':'draft'})

	def button_approve(self):
		picking = []
		for picking_type in self.env['stock.picking.type'].search([('company_id', '=', self.company_id.id),('sequence_code', '=', 'DOUT')]):
			picking_id = self.env['stock.picking'].create({
				'picking_type_id' : picking_type.id,
				'state' : 'draft',
				'origin' : self.name,
				'scheduled_date' : fields.Datetime.now(),
				'company_id' : self.env.user.company_id.id,
				'date' : fields.Datetime.now(),
				'demo_id' : self.id,
				'partner_id' : self.partner_id.id,
				'location_id' : picking_type.default_location_src_id.id,
				'location_dest_id' : picking_type.default_location_dest_id.id,
				})
			rec = self.product_ids.filtered(lambda x: x.demo_id.id == self.id)
			for vals in rec:
				picking.append(picking_id.id)
				stock_line = self.env['stock.move']
				stock_line_obj = stock_line.create({
				   'product_id': vals.product_id.id,
				   'product_uom_qty': vals.product_qty,
				   'picking_id': picking_id.id,
				   'name': self.name,
				   'product_uom': vals.product_id.uom_id.id,
				   'location_id' : picking_type.default_location_src_id.id,
				   'location_dest_id' : picking_type.default_location_dest_id.id,
				   })
				for pick in stock_line_obj:
					pick.mapped('picking_id').filtered(lambda picking: picking.state == 'draft').action_confirm()
		self.write({'state':'approve'})

	def button_reject(self):
		current_employee = self.env.uid
		is_app1 = self.employee_id.rsm_id.user_id.id
		if current_employee == is_app1 or self.env.user._is_admin():
			form_view = self.env.ref('indglobal_events.form_reject_remark_wizard')
			return {
				'name': "Approver Remarks",
				'view_mode': 'form',
				'view_type': 'form',
				'view_id': form_view.id,
				'res_model': 'demo.reject.remark',
				'type': 'ir.actions.act_window',
				'target': 'new',
				'context': {
					'demo_id': self.ids, 'is_reject': True
				}
			}
		elif current_employee != is_app1:
			raise UserError(_('You are not a authorized user to perform actions in this document.'))

	def button_product_sent(self):
		self.write({'state':'product_sent'})

	def button_product_receive(self):
		self.write({'state':'product_received'})

	def _cron_expiry_notify(self):
		for vals in self.env['demo.inventory'].sudo().search([('state', 'in', ['product_sent'])]):
			end_date = vals.end_date - relativedelta(days=1)
			today = date.today()
			if today >= end_date:
				# Email (STARTS)
				template_id = self.env.ref('indglobal_events.email_template_sales_person_expiry_notify')
				template_id.sudo().send_mail(vals.id, force_send=True)
	
class EventCategory(models.Model):
	_name = 'event.category'
	_description = 'Event Category'

	name = fields.Char(string="Name")

class SpecificationDetails(models.Model):
	_name = 'specification.details'
	_description = 'Specification details'

	name = fields.Char(string="Name")
	demo_id = fields.Many2one('demo.inventory', string="Demo")
	spec1_id = fields.Many2one('specification.master', string="Specification1")
	spec2_id = fields.Many2one('specification.master', string="Specification2")
	spec3_id = fields.Many2one('specification.master', string="Specification3")
	spec4_id = fields.Many2one('specification.master', string="Specification4")

class SpecificationMaster(models.Model):
	_name = 'specification.master'
	_description = 'Specification Master'

	name = fields.Char(string="Name")

class ProdutCategory(models.Model):
	_name = 'product.details'
	_description = 'Product Details'

	name = fields.Char(string="Name")
	state = fields.Selection([('draft', 'Draft'), ('request', 'Request'),('approve', 'Approved'), 
		('reject', 'Rejected'),('product_sent', 'Product Sent'), ('product_received', 'Product Received')],
	 string="State", track_visibility='onchange', default="draft", related="demo_id.state")
	demo_id = fields.Many2one('demo.inventory', string="Demo")
	product_id = fields.Many2one('product.product', 'Product', required=True)
	product_qty = fields.Float(string="Product Qty", required=True)

	@api.onchange('product_id')
	def onchange_validity_days(self):
		if self.product_id:
			for var in self.env['product.details'].search([('product_id', '=', self.product_id.id),('state', '!=', 'reject')]):
				if var.demo_id.partner_id.id == self.demo_id.partner_id.id:
					raise ValidationError(_('Already created demo product for this Customer'))




