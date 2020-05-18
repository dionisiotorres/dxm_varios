# -*- coding: utf-8 -*-
{
    'name': "Oct Reception",
    'version': '11.0',  
    'summary': "Create picking from this module",
    'category': "Stock",
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/oct_data.xml',
        'views/oct_reception_view.xml',
    ],
    'installable': True,
    'application': True,
}
