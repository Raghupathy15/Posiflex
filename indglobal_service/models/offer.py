from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError,UserError

class Offers(models.Model):
	_name = "offers"
	_inherit = 'mail.thread'
	_description = 'Offers'

	offer_sequence = fields.Char(default="New", readonly=True, track_visibility='always')
	name = fields.Char('Offer Title',required=True,track_visibility='always')
	description = fields.Char('Offer Desc',track_visibility='always')
	created_date = fields.Date('Created Date',readonly=True,default=fields.Date.today())
	offer_from = fields.Date('Offer From',required=True,track_visibility='always')
	offer_to = fields.Date('Offer To',required=True,track_visibility='always')
	state = fields.Selection([('draft', 'Draft'),('active', 'Active'), ('expired', 'Expired')],string="Status", track_visibility='onchange', default="draft")

	_sql_constraints = [('name', 'UNIQUE (name)', '"Offer Title" must be unique !')]

	@api.model
	def create(self,vals):
		vals['offer_sequence'] = self.env['ir.sequence'].next_by_code('offers') or _('New')
		return super(Offers, self).create(vals)

	@api.constrains('offer_from','offer_to')
	def _check_offer(self):
		for rec in self:
			if rec.offer_from:
				if rec.offer_from > rec.offer_to:
					raise ValidationError(_('"Offer To" date should not be greater than "Offer From" date.'))

	def button_submit(self):
		self.write({'state':'active'})

	def _cron_offer_expiry(self):
		for vals in self.env['offers'].sudo().search([('state', '=', 'active')]):
			curr_date = fields.Date.today()
			if vals.offer_to < fields.Date.today():
				vals.state = 'expired'