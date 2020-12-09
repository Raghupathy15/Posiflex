# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare

class AccountJournal(models.Model):
	_inherit = "account.journal"

	bal_accnt_no = fields.Char('Bal Account No')
	pmt_export = fields.Char('Pmt Export Line Definition')
	bank_pmt_type = fields.Char('Bank Data Conversion Pmt Type')
	pmt_terms_code = fields.Char('Direct Debit Pmt Terms Code')
	payment_processor = fields.Char('Payment processor')
	bal_acnt_type = fields.Selection([('g/l', 'G?L account'),
		('bank','Bank Account')],string='Balance Account Type')
	direct_debit = fields.Boolean('Direct debit')