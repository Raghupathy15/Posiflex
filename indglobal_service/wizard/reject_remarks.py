# -*- coding: utf-8 -*-
from odoo import fields, models, api

class TicketRejectRemark(models.TransientModel):
	_name = 'ticket.reject.remark'
	_description = 'Rejection Remark'

	name = fields.Text('Rejection Remarks')

	def action_ticket_reject_remark(self):
		active_id = self.env.context.get('active_id')
		rec = self.env['tickets'].browse(int(active_id))
		rec.write({'rej_remarks':self.name,'state':'reject'})