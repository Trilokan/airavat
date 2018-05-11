# -*- coding: utf-8 -GPK*-

{
    'name': 'Honey',
    'version': '1.0',
    "author": 'Honey Drop',
    "website": 'http://www.honeydrop.in',
    'category': 'Hospital Management System',
    'sequence': 1,
    'summary': 'Hospital Management System',
    'description': 'Hospital Management System',
    'depends': ['base', 'mail'],
    'data': [
        'views/base_pack/company.xml',
        'views/base_pack/users.xml',
        'menu/main.xml',
        'views/account/period.xml',
        'menu/account.xml',
        'views/employee/employee.xml',
        'menu/employee.xml',

    ],
    'demo': [

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
