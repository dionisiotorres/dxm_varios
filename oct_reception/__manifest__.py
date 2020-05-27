# -*- coding: utf-8 -*-
{
    'name': "Commodity Reception",
    'version': '11.0',  
    'summary': "Logistic Commodity Reception",
    'category': "Stock",
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/oct_data.xml',
        'data/report_paper_format.xml',
        'views/oct_reception_view.xml',
        'report/reception_label_template.xml',
        'report/reception_label.xml'
    ],
    'installable': True,
    'application': False,
}
