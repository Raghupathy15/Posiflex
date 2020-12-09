
{
    'name': 'HR Employee',
    'version': '12.0.2.0.0',
    'summary': """Customization In Employee Master""",
    'description': 'This module helps you to add more information in employee records.',
    'category': 'Generic Modules/Human Resources',
    'author': 'Indglobal digital private limited',
    'company': 'Indglobal digital private limited',
    'website': "https://indglobal.in",
    'depends': ['base', 'hr'],
    'data': [
        'security/hr_security.xml',
        'views/hr_employee_view.xml',
    ],
    'demo': [],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
