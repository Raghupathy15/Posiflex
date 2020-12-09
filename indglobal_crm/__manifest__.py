{
'name' : 'CRM Custom',
'version' : '12.0',
'author' : 'Indglobalal digital private limited',
'website' : 'http://www.indglobal.in',
'category' : 'Tools',
'depends' : ['base', 'crm','sale_crm','indglobal_masters','indglobal_employee'],
'description' : 'CRM Custom',
'data' : [
		'security/crm_security.xml',
		'views/crm_lead.xml',
		'views/crm_lead_to_opportunity_views.xml',
		'data/email_templates.xml',
		'security/ir.model.access.csv',
	],
'installable': True
}