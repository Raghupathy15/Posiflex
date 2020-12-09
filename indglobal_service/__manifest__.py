{
    'name': 'Indglobal Service',
    'version': '13.0',
    'summary': 'Service Management',
    'description': """Service Management""",
    'category': 'Service',
    'author': 'Indglobal Digital Private Limited',
    'depends': ['base','mail','product','stock','sale'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizard/reject_remark_view.xml',
        # 'data/email_templates.xml',
        'data/cron.xml',
        'views/tickets_views.xml',
        'views/sale_order_view.xml',
        'views/offer_views.xml',
        'views/labour_claim_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
