# -*- coding: utf-8 -*-

{
    'name': "Sale Sell Mobile Devices",

    'summary': """
        Custom module to sell mobile devices in the eCommerce
        """,

    'description': """
        Custom module to sell mobile devices in the eCommerce
    """,

    'author': "Heyner Roque | Octupus Technologies SL",
    'website': "https://www.octupus.es",

    'category': 'productivity',
    'version': '0.1',

    'depends': ['base', 'website_sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'application': False,
}
