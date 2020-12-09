# -*- coding: utf-8 -*-
from odoo import fields, models, api

# Demo Rejection Remark

class DemoRejectRemark(models.TransientModel):
	_name = 'demo.reject.remark'
	_description = 'Rejection Remark'

	name = fields.Text('Rejection Remarks')
	employee_id = fields.Many2one('hr.employee', string='Employee', related="demo_id.employee_id")
	demo_id = fields.Many2one('demo.inventory', 'Demo')

	def action_demo_approver_remark(self):
		if self._context.get('is_reject'):
			for demo_id in self.env['demo.inventory'].browse(self._context.get('demo_id', False)):
				demo_id.write({'reject_remarks': self.name, 'state': 'reject'})
				

