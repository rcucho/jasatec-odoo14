# -*- coding: utf-8 -*-
{
    'name': 'Jasatec - Mstech',
    'version': '14.0.1.0.0',
    'author': 'MSTECH',
    'category' : 'Technical Configuration',
    'website': 'http://www.mstech.pe',
    'depends': [
        'industry_fsm',
        'sale',
        'product',
        'stock',
    ],
    'data': [
        'views/view_project_task.xml',
        'views/report_jasatec_contract.xml',
        'report/report_sale_contract.xml',
        'report/report_sale_arrendamiento.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'sequence': 1,
}
