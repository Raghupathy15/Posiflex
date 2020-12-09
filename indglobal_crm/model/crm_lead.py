from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError,UserError

class Lead(models.Model):
	_inherit = "crm.lead"
	_description = "Lead/Opportunity"

	@api.model
	def create(self,vals):
		vals['lead_sequence'] = self.env['ir.sequence'].next_by_code('crm.lead') or _('New')
		vals['opp_sequence'] = self.env['ir.sequence'].next_by_code('crm.lead.opp') or _('New')
		return super(Lead, self).create(vals)

	def write(self, values):
		res =  super(Lead, self).write(values)
		if not self.opp_sequence:
			values['opp_sequence'] = self.env['ir.sequence'].next_by_code('crm.lead.opp') or _('New')
		# To get qty changes in line item to log note
		for line in self:
			msg = "<b>" + _("Quantity has been updated.") + "</b><ul>"
			for crm_line in line.product_ids:
				if crm_line.is_qty_updated == True and crm_line.product_uom_qty_ref == 0.00:
					msg += "<li> %s:" % (crm_line.product_id.display_name,)
					if crm_line.product_uom_qty:
						msg += "<br/>" + _("Quantity") + ": %s -> %s <br/>" % (crm_line.product_uom_qty_ref_1,crm_line.product_uom_qty)
						line.message_post(body=msg)
						crm_line.is_qty_updated = False
						crm_line.product_uom_qty_ref = crm_line.product_uom_qty
				else:
					if crm_line.is_qty_updated == True and crm_line.product_uom_qty_ref != 0.00:
						msg += "<li> %s:" % (crm_line.product_id.display_name,)
						if crm_line.product_uom_qty:
							msg += "<br/>" + _("Quantity") + ": %s -> %s <br/>" % (crm_line.product_uom_qty_ref,crm_line.product_uom_qty)
							line.message_post(body=msg)
							crm_line.is_qty_updated = False
							crm_line.product_uom_qty_ref = crm_line.product_uom_qty
		return res		

	def _compute_user(self):
		user_group= self.env['res.users'].has_group('indglobal_employee.group_hr_partner')
		var = self.env.uid
		for rec in self:
			if user_group:
				rec.is_user = True
			else:
				rec.is_user =False

	name = fields.Char('Opportunity', required=True, index=True,track_visibility='always')
	q_remarks = fields.Text("Qualification Remarks")
	file_upload = fields.Binary("file upload")
	notes = fields.Text("Notes/Requirements")
	cus_remarks = fields.Text("Customer Remarks")
	pre_sales = fields.Boolean('Is Pre-sales ?')
	is_mail_send = fields.Boolean('Is mail send')
	is_user = fields.Boolean('Is User ?',compute=_compute_user)
	
	# Relational fields
	question_line_ids = fields.One2many('questions', 'header_id')
	follow_up_ids = fields.One2many('followup.activities', 'header_id',string='Follow-up Activities')
	partner_follow_up_ids = fields.One2many('followup.activities.partner', 'header_id',string='Follow-up Activities')
	product_ids = fields.One2many('crm.products', 'header_id',string='Product Details')
	user_id = fields.Many2one('res.users', string='Salesperson / Partner',default=False)
	######################
	rsm_id = fields.Many2one('res.users','RSM')
	sm_id = fields.Many2one('res.users','Sales Manager')
	sales_head_id = fields.Many2one('res.users','Sales Head')
	#######################
	rsm_emp_id = fields.Many2one('hr.employee','RSM',track_visibility='always',domain="[('user_level', '=','rsm')]")
	sm_emp_id = fields.Many2one('hr.employee','Sales Manager',track_visibility='always',domain="[('user_level', '=','sm')]")
	sh_emp_id = fields.Many2one('hr.employee','Sales Head',track_visibility='always',domain="[('user_level', '=','sales_head')]")
	pre_sales_id = fields.Many2one('res.users','Pre-sales person')
	pre_sales_person_id = fields.Many2one('res.users','Internal sales person')
	branch_id = fields.Many2one('branch.master','Branch')
	lead_sequence = fields.Char(string="Sequence", readonly=True, track_visibility='always')
	opp_sequence = fields.Char(string="Sequence", readonly=True, track_visibility='always')
	no_of_categ = fields.Selection([('1', '1'),('2', '2'),('3', '3')],string='No of Category')
	categ_id = fields.Many2one('product.category',string="Product category")
	categ_id_1 = fields.Many2one('product.category',string="Product category")
	categ_id_2 = fields.Many2one('product.category',string="Product category")
	categ_id_3 = fields.Many2one('product.category',string="Product category")
	categ_id_4 = fields.Many2one('product.category',string="Product category")
	categ_id_5 = fields.Many2one('product.category',string="Product category")
	categ_id_6 = fields.Many2one('product.category',string="Product category")
	categ_id_7 = fields.Many2one('product.category',string="Product category")
	categ_id_8 = fields.Many2one('product.category',string="Product category")
	categ_id_9 = fields.Many2one('product.category',string="Product category")
	categ_id_10 = fields.Many2one('product.category',string="Product category")
	prod_details_1 = fields.Char(string="Product details",track_visibility='onchange')

	category_ids = fields.Many2many('product.category', string="Product category")


	industry_id = fields.Many2one('industry.master',string="Industry")
	is_won = fields.Boolean('Is Won',compute='_compute_is_won')
	is_quotation_created = fields.Boolean('Is Quotation Created')
	is_sm = fields.Boolean('Is SM',compute='_compute_sm')
	is_rsm = fields.Boolean('Is RSM',compute='_compute_sm')
	is_internal = fields.Boolean('Is Internal Sales Person',compute='_compute_sm')
	is_internal = fields.Boolean('Is Internal Sales Person',compute='_compute_sm')
	email_from = fields.Char('Email', help="Email address of the contact", tracking=40, index=True, required=True)
	partner_name = fields.Char("Company Name",required=True, tracking=20, index=True, help='The name of the future partner company that will be created while converting the lead into opportunity')
	city = fields.Char('City',required=True)
	state_id = fields.Many2one("res.country.state", string='State',required=True)

	def _compute_is_won(self):
		for rec in self:
			if rec.stage_id.is_won == True and self.active == True:
				rec.is_won = True
			else:
				rec.is_won = False

	def _compute_sm(self):
		sm_group= self.env['res.users'].has_group('indglobal_employee.group_hr_sm')
		rsm_group= self.env['res.users'].has_group('indglobal_employee.group_hr_rsm')
		internal_group= self.env['res.users'].has_group('indglobal_employee.group_hr_internal_sales_person')
		var = self.env.uid
		for rec in self:
			if sm_group:
				rec.is_sm = True
			else:
				rec.is_sm = False
			if internal_group:
				rec.is_internal = True
			else:
				rec.is_internal = False
			if rsm_group:
				rec.is_rsm = True
			else:
				rec.is_rsm = False

	# To pass product from CRM to sale quotaion
	def action_create_quotation(self):
		if not self.sm_emp_id.user_id == self.env.user and not self.user_id == self.env.user:
			raise UserError('Only Partner or Sales Manager can create "New Quotation" !!!')
		sale_obj=self.env['sale.order']
		sale_line_obj=self.env['sale.order.line']
		order_lines = []
		for line in self.product_ids:
			order_lines.append((0,0,{'product_id': line.product_id.id,
				'name': line.product_id.prod_description,
				'product_uom_qty':line.product_uom_qty,
				'warranty_period':line.product_id.warranty_period,
			}))
		if self.partner_id and self.user_id:
			sale_id = sale_obj.create({
				'partner_id':self.partner_id.id,
				'team_id': self.team_id.id,
				'campaign_id': self.campaign_id.id,
				'medium_id': self.medium_id.id,
				'source_id': self.source_id.id,
				'order_line':order_lines,
				'crm_id':self.id,
				'sm_emp_id':self.sm_emp_id.id,
				'rsm_emp_id':self.rsm_emp_id.id,
				'sh_emp_id':self.sh_emp_id.id,
				'sale_type':'from_crm',
				'user_id':self.user_id.id,
				'contact_name':self.contact_name,
				'street':self.street,
				'street2':self.street2,
				'zip':self.zip,
				'city':self.city,
				'state_id':self.state_id.id,
				'country_id':self.country_id.id,
				'phone':self.phone,
				'mobile':self.mobile,
			})
			self.write({'is_quotation_created': True})
		elif not self.partner_id and not self.user_id:
			sale_id = sale_obj.create({
				'partner_id':42,
				'team_id': self.team_id.id,
				'campaign_id': self.campaign_id.id,
				'medium_id': self.medium_id.id,
				'source_id': self.source_id.id,
				'order_line':order_lines,
				'crm_id':self.id,
				'user_id':self.env.user.id,
				'sm_emp_id':self.sm_emp_id.id,
				'rsm_emp_id':self.rsm_emp_id.id,
				'sale_type':'from_crm',
				'sh_emp_id':self.sh_emp_id.id,
				'contact_name':self.contact_name,
				'street':self.street,
				'street2':self.street2,
				'zip':self.zip,
				'city':self.city,
				'state_id':self.state_id.id,
				'country_id':self.country_id.id,
				'phone':self.phone,
				'mobile':self.mobile,
			})
			self.write({'is_quotation_created': True})
		elif self.partner_id and not self.user_id:
			sale_id = sale_obj.create({
				'partner_id':self.partner_id.id,
				'team_id': self.team_id.id,
				'campaign_id': self.campaign_id.id,
				'medium_id': self.medium_id.id,
				'source_id': self.source_id.id,
				'order_line':order_lines,
				'crm_id':self.id,
				'user_id':self.env.user.id,
				'sm_emp_id':self.sm_emp_id.id,
				'rsm_emp_id':self.rsm_emp_id.id,
				'sale_type':'from_crm',
				'sh_emp_id':self.sh_emp_id.id,
				'contact_name':self.contact_name,
				'street':self.street,
				'street2':self.street2,
				'zip':self.zip,
				'city':self.city,
				'state_id':self.state_id.id,
				'country_id':self.country_id.id,
				'phone':self.phone,
				'mobile':self.mobile,
			})
			self.write({'is_quotation_created': True})
		elif not self.partner_id and self.user_id:
			sale_id = sale_obj.create({
				'partner_id':42,
				'team_id': self.team_id.id,
				'campaign_id': self.campaign_id.id,
				'medium_id': self.medium_id.id,
				'source_id': self.source_id.id,
				'order_line':order_lines,
				'crm_id':self.id,
				'user_id':self.user_id.id,
				'sm_emp_id':self.sm_emp_id.id,
				'rsm_emp_id':self.rsm_emp_id.id,
				'sale_type':'from_crm',
				'sh_emp_id':self.sh_emp_id.id,
				'contact_name':self.contact_name,
				'street':self.street,
				'street2':self.street2,
				'zip':self.zip,
				'city':self.city,
				'state_id':self.state_id.id,
				'country_id':self.country_id.id,
				'phone':self.phone,
				'mobile':self.mobile,
			})
			self.write({'is_quotation_created': True})
		return True

	def send_mail_to_sales(self):
		if self.is_mail_send == False:
			template_id = self.env.ref('indglobal_crm.email_template_sales_person')
			template_id.sudo().send_mail(self.id, force_send=True)
			self.write({'is_mail_send': True})

	@api.onchange('user_id')
	def onchange_is_mail_send(self):
		if self.user_id and self.is_mail_send == True:
			self.is_mail_send = False

	# @api.onchange('categ_id')
	# def onchange_categ_id(self):
	# 	if self.categ_id:
	# 		master = self.env['questions.master'].search([('categ_id', '=', self.categ_id.id)])
	# 		if master:
	# 			if master.categ_id.id == self.categ_id_1.id or master.categ_id.id == self.categ_id_2.id or master.categ_id.id == self.categ_id_3.id or master.categ_id.id == self.categ_id_4.id or master.categ_id.id == self.categ_id_5.id or master.categ_id.id == self.categ_id_6.id or master.categ_id.id == self.categ_id_7.id or master.categ_id.id == self.categ_id_8.id or master.categ_id.id == self.categ_id_9.id or master.categ_id.id == self.categ_id_10.id:
	# 				raise UserError(_('You can not select same category for multiple times'))
	# 			if not self.categ_id_1:
	# 				self.categ_id_1 = master.categ_id.id
	# 			elif not self.categ_id_2:
	# 				self.categ_id_2 = master.categ_id.id
	# 			elif not self.categ_id_3:
	# 				self.categ_id_3 = master.categ_id.id
	# 			elif not self.categ_id_4:
	# 				self.categ_id_4 = master.categ_id.id
	# 			elif not self.categ_id_5:
	# 				self.categ_id_5 = master.categ_id.id
	# 			elif not self.categ_id_6:
	# 				self.categ_id_6 = master.categ_id.id
	# 			elif not self.categ_id_7:
	# 				self.categ_id_7 = master.categ_id.id
	# 			elif not self.categ_id_8:
	# 				self.categ_id_8 = master.categ_id.id
	# 			elif not self.categ_id_9:
	# 				self.categ_id_9 = master.categ_id.id
	# 			elif not self.categ_id_10:
	# 				self.categ_id_10 = master.categ_id.id
	# 			for line in master.questions_line_ids:
	# 				create_rec = self.env['questions'].create({'name':line.name,
	# 															'categ_id':master.categ_id.id,
	# 															'header_id':self.id})

	@api.onchange('category_ids')
	def onchange_category(self):
		if self.category_ids:
			for rec in self.category_ids:
				for vals in self.env['questions.master'].sudo().search([('categ_id.name', '=',rec.name)]):
					if vals:
						print ('11111111111',vals)
						for line in vals.questions_line_ids:
							create_rec = self.env['questions'].create({'name':line.name,
																		'categ_id':vals.categ_id.id,
																		'header_id':self.id})
					else:
						print ('222222222',vals)
						rec = unlink()

	@api.onchange('sm_emp_id')
	def onchange_rsm_sh(self):
		if self.sm_emp_id:
			self.rsm_emp_id = self.sm_emp_id.rsm_id.id
			self.sh_emp_id = self.sm_emp_id.sales_head_id.id

	@api.onchange('rsm_emp_id')
	def onchange_sh(self):
		if self.rsm_emp_id:
			self.sh_emp_id = self.rsm_emp_id.sales_head_id.id

	@api.onchange('user_id')
	def onchange_user_id(self):
		if self.user_id:
			self.sm_emp_id = self.user_id.sales_manager_id.id

class Questions(models.Model):
	_name = 'questions'
	_description = "Set of Questions - CRM"

	name = fields.Text("Questions")
	answer = fields.Text("Answer")
	categ_id = fields.Many2one('product.category', 'Product category',readonly=True)
	header_id = fields.Many2one('crm.lead')

class FollowupActivities(models.Model):
	_name = 'followup.activities'
	_description = "Follow-up Activities"

	activity_type_id = fields.Many2one('mail.activity.type', 'Activity Type',required=True)
	user_id = fields.Many2one('res.users',string='Assigned to',default=lambda self:self.env.user,readonly=True)
	update_user_id = fields.Many2one('res.users',string='Last updated By',readonly=True)
	name = fields.Char('Description')
	summary = fields.Char('Summary')
	date = fields.Date('Due Date',index=True)
	sequence_no = fields.Char(string="Sequence", default="New")
	header_id = fields.Many2one('crm.lead')

	@api.onchange('date','activity_type_id','name')
	def onchange_update_user_id(self):
		if self.date:
			self.update_user_id=self.env.user

class FollowupActivitiesPartner(models.Model):
	_name = 'followup.activities.partner'
	_description = "Follow-up Activities for Partner"

	partner_activity_id = fields.Many2one('mail.activity.type', 'Activity',required=True)
	name = fields.Char('Description')
	date = fields.Date('Follow-up Date',index=True, default=fields.Date.context_today)
	header_id = fields.Many2one('crm.lead')

class CRMProducts(models.Model):
	_name = 'crm.products'
	_description = "Product Details - CRM"

	name = fields.Char('Description')
	product_id = fields.Many2one('product.product', 'Product Name',required=True)
	categ_id = fields.Many2one('product.category', 'Product category',readonly=True)
	product_uom_qty = fields.Float('Quantity')
	#########3
	product_uom_qty_ref = fields.Float('Quantity')
	product_uom_qty_ref_1 = fields.Float('Qty')
	is_qty_updated = fields.Boolean('Qty Updated')
	header_id = fields.Many2one('crm.lead')

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
			if product.product_uom_qty:
				qty = product.product_uom_qty % 1
				if qty != 0:
					raise UserError('Quantity should in whole number')

	@api.onchange('product_id')
	def onchange_product_id(self):
		for rec in self:
			if rec.product_id:
				rec.categ_id = rec.product_id.categ_id.id
				rec.name = rec.product_id.name

	@api.onchange('product_uom_qty')
	def onchange_product_qty(self):
		for rec in self:
			if rec.product_uom_qty_ref_1 == 0:
				rec.is_qty_updated = False
			if rec.product_uom_qty_ref_1 != 0:
				rec.is_qty_updated = True
			if rec.product_uom_qty_ref_1 < 1:
				rec.product_uom_qty_ref_1 = rec.product_uom_qty