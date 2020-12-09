from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError,UserError

class SaleOrder(models.Model):
	_inherit = "sale.order"

	def _default_validity_date(self):
		if self.env['ir.config_parameter'].sudo().get_param('sale.use_quotation_validity_days'):
			days = self.env.company.quotation_validity_days
			if days > 0:
				return fields.Date.to_string(datetime.now() + timedelta(days))
		return False

	# To change the string name
	validity_date = fields.Date(string='Quotation Validity', readonly=True, copy=False, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
								default=_default_validity_date)
	state = fields.Selection([
		('draft', 'Quotation'),
		('sent', 'Quotation Sent'),
		('sale', 'Sales Order'),
		('discount_request', 'Discount Request'),
		('dis_app_sm', 'Discount Approved by SM'),
		('dis_app_rsm', 'Discount Approved by RSM'),
		('dis_app_sh', 'Discount Approved by Sales Head'),
		('dis_req_cancelled', 'Discount Request Cancelled'),
		('done', 'Locked'),
		('cancel', 'Cancelled'),
		], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
	rej_remarks=fields.Text("Discount request rejected Remarks",track_visibility='always')
	rej_by=fields.Many2one('res.user',"Discount request rejected By",track_visibility='always')
	attachment_ids = fields.One2many('upload.invoice', 'header_id',string='Invoice Attachments')
	user_id = fields.Many2one('res.users', string='Salesperson / Partner', index=True, tracking=2,required=False)
	rsm_emp_id = fields.Many2one('hr.employee','RSM',required=False,track_visibility='always',domain="[('user_level', '=','rsm')]")
	sm_emp_id = fields.Many2one('hr.employee','Sales Manager',required=False,track_visibility='always',domain="[('user_level', '=','sm')]")
	sh_emp_id = fields.Many2one('hr.employee','Sales Head',required=False,track_visibility='always',domain="[('user_level', '=','sales_head')]")
	is_rsm = fields.Boolean('Is RSM',compute='_compute_user')
	is_sm = fields.Boolean('Is SM',compute='_compute_user')
	is_sales_head = fields.Boolean('Is SH',compute='_compute_user')
	is_dis_approved = fields.Boolean('Is Discount Approved')
	crm_id = fields.Many2one('crm.lead','CRM Reference')
	sale_type = fields.Selection([ ('from_crm', 'From CRM'),
		('direct', 'Direct')],string='Sale Type', readonly=True,default='direct')
	
	# Address fields
	contact_name = fields.Char('Contact Name')
	street = fields.Char('Street')
	street2 = fields.Char('Street2')
	zip = fields.Char('Zip', change_default=True)
	city = fields.Char('City')
	state_id = fields.Many2one("res.country.state", string='State',required=True)
	country_id = fields.Many2one('res.country', string='Country')
	phone = fields.Char('Phone',)
	mobile = fields.Char('Mobile')

	@api.constrains('order_line')
	def _check_exist_product_in_line(self):
		for sale in self:
			exist_product_list = []
			for line in sale.order_line:
				if line.product_id.id in exist_product_list:
					raise ValidationError(_('Product should be one per line.'))
				exist_product_list.append(line.product_id.id)

	def action_confirm(self):
		if self.contact_name:
			partner = self.env['res.partner'].search([('name','=',self.contact_name)])
			if not partner:
				create_rec = self.env['res.partner'].create({'name':self.contact_name,
															'street':self.street,
															'street2':self.street2,
															'zip':self.zip,
															'city':self.city,
															'state_id':self.state_id.id,
															'country_id':self.country_id.id,
															'phone':self.phone,
															'mobile':self.mobile})
				rec = self.env['res.partner'].search([('name','=',self.contact_name)])
				if rec:
					self.partner_id = rec
		record = super(SaleOrder, self).action_confirm()

	@api.onchange('partner_id')
	def _onchange_partner_id(self):
		if self.partner_id:
			self.street = self.partner_id.street
			self.street2 = self.partner_id.street2
			self.zip = self.partner_id.zip
			self.city = self.partner_id.city
			self.state_id = self.partner_id.state_id.id
			self.country_id = self.partner_id.country_id.id
			self.phone = self.partner_id.phone
			self.mobile = self.partner_id.mobile
		if not self.sm_emp_id:
			sm_group= self.env['res.users'].has_group('indglobal_employee.group_hr_sm')
			rsm_group= self.env['res.users'].has_group('indglobal_employee.group_hr_rsm')
			sh_group= self.env['res.users'].has_group('indglobal_employee.group_hr_sales_head')
			if sm_group == True:
				emp = self.env['hr.employee'].search([('user_id','=',self.env.uid)])
				if emp:
					self.sm_emp_id = emp.id
			if rsm_group == True:
				emp = self.env['hr.employee'].search([('user_id','=',self.env.uid)])
				if emp:
					self.rsm_emp_id = emp.id
					self.sh_emp_id = emp.sales_head_id.id
			if sh_group == True and not self.sh_emp_id:
				emp = self.env['hr.employee'].search([('user_id','=',self.env.uid)])
				if emp:
					self.sh_emp_id = emp.id

	@api.onchange('country_id')
	def _onchange_country_id(self):
		if self.country_id and self.country_id != self.state_id.country_id:
			self.state_id = False

	@api.onchange('state_id')
	def _onchange_state(self):
		if self.state_id.country_id:
			self.country_id = self.state_id.country_id

	@api.onchange('user_id','rsm_emp_id','sm_emp_id','sh_emp_id')
	def onchange_user_details(self):
		if self.sm_emp_id:
			self.rsm_emp_id = self.sm_emp_id.rsm_id.id
			self.sh_emp_id = self.sm_emp_id.sales_head_id.id

	def _compute_user(self):
		if self.user_id:
			for data in self:
				if data.rsm_emp_id.user_id.id == self.env.uid:
					data.is_rsm = True
				else:
					data.is_rsm = False
				if data.sm_emp_id.user_id.id == self.env.uid:
					data.is_sm = True
				else:
					data.is_sm = False
				if data.sh_emp_id.user_id.id == self.env.uid:
					data.is_sales_head = True
				else:
					data.is_sales_head = False

	def button_dis_req(self):
		for rec in self:
			if not rec.order_line:
				raise ValidationError(_('Without product line you can not raise discount request.'))
		if self.is_sm == True:
			self.write({'state':'dis_app_sm'})
			template_id = self.env.ref('indglobal_sale.email_template_disc_req_created_rsm')
			template_id.sudo().send_mail(self.id, force_send=True)
		else:
			self.write({'state':'discount_request'})
			template_id = self.env.ref('indglobal_sale.email_template_disc_req_created')
			template_id.sudo().send_mail(self.id, force_send=True)

	def button_app_dic_by_sm(self):
		self.write({'state':'dis_app_sm'})
		template_id = self.env.ref('indglobal_sale.email_template_disc_req_created_rsm')
		template_id.sudo().send_mail(self.id, force_send=True)

	def button_app_dic_by_rsm(self):
		self.write({'state':'dis_app_rsm'})
		template_id = self.env.ref('indglobal_sale.email_template_disc_req_created_sm')
		template_id.sudo().send_mail(self.id, force_send=True)

	def button_app_dic_by_sh(self):
		self.write({'state':'dis_app_sh'})
		template_id = self.env.ref('indglobal_sale.email_template_sales_person_dis_approved')
		template_id.sudo().send_mail(self.id, force_send=True)

	def button_cancel_req(self):
		form_view = self.env.ref('indglobal_sale.cancel_details_view_id')
		return {
				'name': "Cancel Remarks",
				'view_mode': 'form',
				'view_type': 'form',
				'view_id': form_view.id,
				'res_model': 'cancel.remarks',
				'type': 'ir.actions.act_window',
				'target': 'new',
			}
class InvoiceAttachment(models.Model):
	_name = 'upload.invoice'
	_description = "Invoice Attachment"

	name = fields.Char('Description')
	user_id = fields.Many2one('res.users',string='Attached By',default=lambda self:self.env.user,readonly=True)
	date = fields.Date('Date',default=fields.Date.context_today,readonly=True)
	existing_invoice=fields.Binary("Attachment")
	att_invoice=fields.Char("Attachment")
	header_id = fields.Many2one('sale.order')