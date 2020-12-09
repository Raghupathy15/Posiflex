from datetime import datetime, timedelta
from odoo import models, fields,api, _

class HrEmployeePrivate(models.Model):
	_inherit = 'hr.employee'

	emp_id = fields.Char(string='Emp ID')
	work_email = fields.Char('Work Email',required=True)
	user_level = fields.Selection([('admin', 'Admin'),('sales_head', 'Sales Head'),('rsm','RSM'),('sm','SM'),
								('partner','Partner'),('internal_sales_person','Internal-sales person')],string='CRM User Level',required=True)
	parent_id = fields.Many2one('hr.employee', 'Sales Manager', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
	rsm_id = fields.Many2one('hr.employee', 'RSM', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
	sales_head_id = fields.Many2one('hr.employee', 'Sales Head', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
	company_ids = fields.Many2many('res.company', 'res_company_emp_rel', 'user_id', 'cid',
					string='Allowed Companies', default=lambda self: self.env.company.ids)

	@api.model
	def create(self, vals):
		res = super(HrEmployeePrivate, self).create(vals)
		if res:
			# create user when create employee
			user_id = self.env['res.users'].create({
				'name': res.name,
				'login': res.work_email,
				'email': res.work_email,
				'sales_manager_id': res.parent_id.id,
				'rsm_id': res.rsm_id.id,
				'sales_head_id': res.sales_head_id.id,
				'password': '123',
				'groups_id': [(4,self.env.ref('base.group_user').id)]
			})
			user_id.write({'groups_id': [(6,0,[self.env.ref('hr.group_hr_user').id])]})	

			if res.user_level == 'admin':
				user_id.write({'groups_id': [(4, self.env.ref('hr.group_hr_manager').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('sales_team.group_sale_manager').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('stock.group_stock_manager').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('purchase.group_purchase_manager').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('base.group_erp_manager').id)]})
			if res.user_level == 'sales_head':
				user_id.write({'groups_id': [(4, self.env.ref('hr.group_hr_manager').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('indglobal_employee.group_hr_sales_head').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('sales_team.group_sale_salesman').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('stock.group_stock_user').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('purchase.group_purchase_user').id)]})
			if res.user_level == 'rsm':
				user_id.write({'groups_id': [(4, self.env.ref('hr.group_hr_manager').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('indglobal_employee.group_hr_rsm').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('sales_team.group_sale_salesman').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('stock.group_stock_user').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('purchase.group_purchase_user').id)]})
			if res.user_level == 'sm':
				user_id.write({'groups_id': [(4, self.env.ref('hr.group_hr_manager').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('indglobal_employee.group_hr_sm').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('sales_team.group_sale_salesman').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('stock.group_stock_user').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('purchase.group_purchase_user').id)]})
			if res.user_level == 'partner':
				user_id.write({'groups_id': [(4, self.env.ref('hr.group_hr_manager').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('indglobal_employee.group_hr_partner').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('sales_team.group_sale_salesman').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('stock.group_stock_user').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('purchase.group_purchase_user').id)]})
			if res.user_level == 'internal_sales_person':
				user_id.write({'groups_id': [(4, self.env.ref('hr.group_hr_manager').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('indglobal_employee.group_hr_internal_sales_person').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('sales_team.group_sale_salesman').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('stock.group_stock_user').id)]})
				user_id.write({'groups_id': [(4, self.env.ref('purchase.group_purchase_user').id)]})
			res.user_id=user_id.id
		return res

	def write(self, values):
		res = super(HrEmployeePrivate, self).write(values)
		user_search = self.env['res.users'].search([('login', '=', self.work_email)])
		if user_search:
			user_details = self.env['res.users'].write({
				'name': user_search.name,
				'login': user_search.work_email,
				'email': user_search.work_email,
				'sales_manager_id': self.parent_id.id
			})
			user_search.write({'sales_manager_id':self.parent_id.id,'rsm_id':self.rsm_id.id,'sales_head_id':self.sales_head_id.id})
			user_search.write({'groups_id': [(6,0, [self.env.ref('hr.group_hr_user').id])]})
			if self.user_level == 'admin':
				user_search.write({'groups_id': [(4, self.env.ref('hr.group_hr_manager').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('sales_team.group_sale_manager').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('stock.group_stock_manager').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('purchase.group_purchase_manager').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('base.group_erp_manager').id)]})
			if self.user_level == 'sales_head':
				user_search.write({'groups_id': [(4, self.env.ref('hr.group_hr_manager').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('indglobal_employee.group_hr_sales_head').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('sales_team.group_sale_salesman').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('stock.group_stock_user').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('purchase.group_purchase_user').id)]})
			if self.user_level == 'rsm':
				user_search.write({'groups_id': [(4, self.env.ref('hr.group_hr_manager').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('indglobal_employee.group_hr_rsm').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('sales_team.group_sale_salesman').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('stock.group_stock_user').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('purchase.group_purchase_user').id)]})
			if self.user_level == 'sm':
				user_search.write({'groups_id': [(4, self.env.ref('hr.group_hr_manager').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('indglobal_employee.group_hr_sm').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('sales_team.group_sale_salesman').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('stock.group_stock_user').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('purchase.group_purchase_user').id)]})
			if self.user_level == 'partner':
				user_search.write({'groups_id': [(4, self.env.ref('hr.group_hr_manager').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('indglobal_employee.group_hr_partner').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('sales_team.group_sale_salesman').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('stock.group_stock_user').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('purchase.group_purchase_user').id)]})
			if self.user_level == 'internal_sales_person':
				user_search.write({'groups_id': [(4, self.env.ref('hr.group_hr_manager').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('indglobal_employee.group_hr_internal_sales_person').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('sales_team.group_sale_salesman').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('stock.group_stock_user').id)]})
				user_search.write({'groups_id': [(4, self.env.ref('purchase.group_purchase_user').id)]})
		return res