# -*- coding: utf-8 -*-

{
    'name': "Serial Batch Import",

    'summary': """
        Import serial numbers from excel file.
        """,

    'description': """
        Import serial numbers from excel file on stock operations.
    """,

    'author': "Heyner Roque | Octupus Technologies SL",
    'website': "https://www.octupus.es",

    'category': 'productivity',
    'version': '0.1',

    'depends': ['base', 'stock'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/actions.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'application': False,
}
