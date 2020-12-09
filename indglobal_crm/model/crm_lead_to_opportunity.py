from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

class Lead2OpportunityPartner(models.TransientModel):
	_inherit = 'crm.lead2opportunity.partner'

	# This inherit is bcas of 'sales person' field and 'sales team' field should be empty by default,
	 # bcas as per requirement this two fields should be invisibled.
	 
	@api.model
	def default_get(self, fields):
		result = super(Lead2OpportunityPartner, self).default_get(fields)
		if self._context.get('active_id'):
			lead = self.env['crm.lead'].browse(self._context['active_id'])
			if lead.user_id:
				result['user_id'] = ''
			if lead.team_id:
				result['team_id'] = ''
		return result

	user_id = fields.Many2one('res.users', 'Salesperson', index=True)
	team_id = fields.Many2one('crm.team', 'Sales Team', index=True)

class PartnerBinding(models.TransientModel):
	_inherit = 'crm.partner.binding'

	action = fields.Selection([
		('create', 'Create a new customer'),
		('exist', 'Link to an existing customer'),
		('nothing', 'Do not link to a customer')
	], 'Related Customer',default='nothing', required=True,readonly=True)
