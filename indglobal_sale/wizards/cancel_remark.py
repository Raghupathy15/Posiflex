# -*- coding: utf-8 -*-
import logging
from odoo import models, api,fields, _
from itertools import groupby
from odoo.exceptions import UserError,ValidationError

class CancelRemarks(models.TransientModel):
	_name = 'cancel.remarks'
	_description = "Cancel Remarks"

	name = fields.Text('Cancel Remarks')

	def action_cancel_remark(self):
		active_id = self.env.context.get('active_id')
		rec = self.env['sale.order'].browse(int(active_id))
		rec.write({'rej_remarks':self.name,'state':'dis_req_cancelled'})
		template_id = rec.env.ref('indglobal_sale.email_template_dis_rej')
		template_id.sudo().send_mail(rec.id, force_send=True)