# -*- coding: utf-8 -*-

{
    'name': "Quality Mobile Test",

    'summary': """
        Quality Mobile Test
        """,

    'description': """
        Quality Mobile Test
    """,

    'author': "Heyner Roque | Octupus Technologies SL",
    'website': "https://www.octupus.es",

    'category': 'productivity',
    'version': '0.1',

    'depends': ['base', 'stock'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/stock_picking_view.xml',
        'views/stock_production_lot.xml',
        'views/res_config.xml',
        'views/functional_quality_test_view.xml',
        'views/esthetic_quality_test_view.xml',
        'wizard/functional_test_view.xml',
        'wizard/esthetic_test_view.xml',
    ],
    'installable': True,
    'application': False,
}
