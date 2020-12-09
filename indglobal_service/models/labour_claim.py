from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError,UserError

class LabourClaimMaster(models.Model):
	_name = "labour.claim.master"
	_inherit = 'mail.thread'
	_description = 'Labour Claim Master'

	name = fields.Many2one('res.users',string='User Name',required=True,track_visibility='always')
	amnt = fields.Integer(string='Amount per day',required=True,track_visibility='always')

	_sql_constraints = [('user_id', 'UNIQUE (user_id)', '"User Name" must be unique !')]

class LabourClaim(models.Model):
	_name = "labour.claim"
	_inherit = 'mail.thread'
	_description = 'Labour Claim'

	name = fields.Many2one('res.users',string='Name',required=True,track_visibility='always',default=lambda self: self.env.user)
	amnt = fields.Integer(string='Amount per day',readonly=True,track_visibility='always')
	no_of_days = fields.Integer(string='No of Days',required=True,track_visibility='always')
	tot_amnt = fields.Integer(string='Total claim Amount',readonly=True,track_visibility='always')
	state = fields.Selection([('draft', 'Draft'), ('claim_requested', 'Requested'),('approved', 'Approved'),
					('reject', 'Rejected')],string="State",track_visibility='onchange',default="draft")
	remarks = fields.Text(string='Remarks')
	rej_remarks = fields.Text(string='Rejection Remarks')

	@api.onchange('name','no_of_days')
	def onchange_customer_id(self):
		master = self.env['labour.claim.master'].sudo().search([('name', '=',self.name.id)])
		if master:
			self.amnt = master.amnt
			self.tot_amnt = self.amnt * self.no_of_days

	def button_submit(self):
		if self.no_of_days < 1:
			raise ValidationError(_('"No of Days" should not be greater than 0.'))
		else:
			self.write({'state':'claim_requested'})

	def button_approve(self):
		self.write({'state':'approved'})

	def button_reject(self):
		form_view = self.env.ref('indglobal_service.claim_details_view_id')
		return {
				'name': "Reject Remarks",
				'view_mode': 'form',
				'view_type': 'form',
				'view_id': form_view.id,
				'res_model': 'claim.reject.remark',
				'type': 'ir.actions.act_window',
				'target': 'new',
			}
