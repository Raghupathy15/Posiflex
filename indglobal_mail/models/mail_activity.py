from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.addons import decimal_precision as dp
import re
from odoo.exceptions import ValidationError

class MailActivity(models.Model):
	_inherit = "mail.activity"

	sequence_no = fields.Char(string="Sequence", track_visibility='always')
	note = fields.Text('Note')

	def action_close_dialog(self):
		for record in self:
			if record.activity_type_id:
				res = self.env['mail.activity'].search([('id','>',0)],order="id desc",limit=1)
				data = res.id-1
				final_id = self.env['mail.activity'].search([('id','=',data)])
				record.sequence_no = int(final_id.sequence_no)+1
			res = activity = super(MailActivity, self).action_close_dialog()