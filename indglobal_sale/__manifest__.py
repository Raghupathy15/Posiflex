# -*- coding: utf-8 -*-
{
	'name' : 'Sale Customization',
	'version' : '1.0',
	'author' : 'Indglobal digital Private Limited',
	'website' : 'http://www.indglobal.in',
	'category' : 'Sale',
	'depends' : ['sale', 'base'],
	'summary': 'Sale Customization',
	'data' : [
		'security/sale_security.xml',
		'security/ir.model.access.csv',
		'views/sale_order_view.xml',
		'wizards/cancel_remark_view.xml',
		'data/email_templates.xml',
		'views/inherit_sale_order_line_view.xml',
		'report/sale_report_templates.xml',
	],
	'installable': True,
	'license': 'LGPL-3',
}