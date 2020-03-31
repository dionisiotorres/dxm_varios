# -*- coding: utf-8 -*-

{
    'name': "Stock Batch Operations",

    'summary': """
        Stock Batch Operations.
        """,

    'description': """
        Stock batch operations like import serial numbers, unpack lots.
    """,

    'author': "Heyner Roque | Octupus Technologies SL",
    'website': "https://www.octupus.es",

    'category': 'productivity',
    'version': '0.1',

    'depends': ['base', 'stock', 'message_popup'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/serial_import_views.xml',
        'views/unpack_lots_views.xml',
    ],
    'installable': True,
    'application': False,
}
