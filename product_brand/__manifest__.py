# -*- coding: utf-8 -*-

{
    'name': "Product Brand",

    'summary': """
        Add product brand
        """,

    'description': """
        Add product brand
    """,

    'author': "Heyner Roque | Octupus Technologies SL",
    'website': "https://www.octupus.es",

    'category': 'productivity',
    'version': '0.1',

    'depends': ['base', 'product', 'sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/product_brand.xml',
        'views/product_template.xml',
    ],
    'installable': True,
    'application': False,
}
