# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models,_
import re
from odoo.exceptions import ValidationError,UserError

class ResPartner(models.Model):
	_inherit = "res.partner"

	customer_id = fields.Char('No')
	fax_no = fields.Char('Fax No')
	telex_answer_back = fields.Char('Telex Answer Back')
	vat_reg_no = fields.Char('VAT Registration No')
	posting_group = fields.Char('Gen. Bus. Posting Group')
	payment_method_code = fields.Char('Payment Method Code')
	vat_posting_group = fields.Char('VAT Bus. Posting Group')
	ic_partner_code = fields.Char('IC Partner Code')
	lead_time_calculation = fields.Char('Lead Time Calculation')
	responsibility_center = fields.Char('Responsibility Center')
	telex_no = fields.Integer('Telex No')
	territory_code = fields.Integer('Territory Code')
	global_dimension_code_1 = fields.Integer('Global Dimension 1 Code')
	global_dimension_code_2 = fields.Integer('Global Dimension 2 Code')
	statistics_group = fields.Integer('Statistics Group')
	payment_terms_code = fields.Integer('Payment Terms Code')
	charge_terms_code = fields.Integer('Fin. Charge Terms Code')
	purchaser_code = fields.Integer('Purchaser Code')
	shipment_method_code = fields.Integer('Shipment Method Code')
	Shipping_agent_code = fields.Integer('Shipping Agent Code')
	invoice_disc_code = fields.Integer('Invoice Disc. Code')
	pay_to_vendor_no = fields.Integer('Pay-to Vendor No')
	priority = fields.Integer('Priority')
	gln = fields.Char('GLN')
	tin = fields.Char('TIN No')
	lst = fields.Char('LST No')
	cst = fields.Char('CST No')
	pan = fields.Char('PAN No')
	pan_ref_no = fields.Char('PAN Ref No')
	ecc = fields.Char('ECC No')
	range = fields.Char('Range')
	commissioner_permission_no = fields.Char('Commissioners Permission No')
	service_tax_registration_no = fields.Char('Service Tax Registration No')
	service_entity_type = fields.Char('Service Entity Type')
	structure = fields.Char('Structure')
	vendor_location = fields.Char('Vendor Location')
	collectorate = fields.Char('Collectorate')
	excise_posting_group = fields.Char('Excise Bus. Posting Group')
	base_calendar_code = fields.Integer('Base Calendar Code')
	gst_reg_no = fields.Integer('GST Registration No')
	creditor_no = fields.Integer('Creditor No')
	location_code = fields.Integer('Location Code')
	preferred_bank_account = fields.Integer('Preferred Bank Account')
	prepayment = fields.Integer('Prepayment %')
	arn_no = fields.Integer('ARN No')
	cash_flow_payment_terms = fields.Integer('Cash Flow Payment Terms Code')
	vat_price = fields.Boolean('Price Including VAT')
	tax_liable = fields.Boolean('Tax Liable')
	ssi = fields.Boolean('SSI')
	block_payment_tolerance = fields.Boolean('Block Payment Tolerance')
	subcontractor = fields.Boolean('Subcontractor')
	privacy_blocked = fields.Boolean('Privacy Blocked')
	composition = fields.Boolean('Composition')
	transporter = fields.Boolean('Transporter')
	associated_enterprises = fields.Boolean('Associated Enterprises')
	budgeted_amt = fields.Float('Budgeted Amount')
	ssi_validity_date = fields.Date('SSI Validity Date')
	application_method = fields.Selection([('manual', 'Manual'),('apply_to_oldest','Apply to oldest')],string='Application Method')
	vendor_type = fields.Selection([('m', 'Manufacturer'),('f','First stage dealer'),
		('s','Second stage dealer'),('i','Importer')],string='Vendor Method')
	pan_status = fields.Selection([('applied', 'Applied'),('invalid','In-Valid'),
		('not_available','Not Available')],string='PAN Status')
	gst_vendor_type = fields.Selection([('registered', 'Registered'),('composite','Composite'),
		('un_registered','Un Registered'),('import','Import'),('exempted','Exempted'),
		('sez','SEZ')],string='GST Vendor Type')
	aggregate_turnover = fields.Selection([('more_than_20', 'More than 20 lakh'),
		('less_than_20','Less than 20 lakh')],string='Aggregate Turnover')
	blocked = fields.Selection([('payment', 'Payment'),
		('all','All')],string='Blocked')
	posting_group_id = fields.Many2one(comodel_name='vendor.groups', string='Vendor Posting Group')
	cus_posting_group_id = fields.Many2one(comodel_name='customer.groups', string='Customer Posting Group')
	# Customer
	acc_no = fields.Char('Our Account No')
	credit_limit = fields.Char('Credit Limit (LYC)')