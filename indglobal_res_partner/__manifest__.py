# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Customer Master',
    'version' : '1.1',
	'author' : 'Indglobal digital private limited',
    'summary': 'Adding additional fields in Customer Master',
    'sequence': 1,
    'description': """Inheriting fields in Customer Master""",
    'category' : 'Contacts',
    'website': 'https://www.indglobal.com',
    'depends' : ['base','indglobal_masters'],
    'data': ['views/res_partner_views.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OEEL-1',
}