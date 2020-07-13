##############################################################################
#
#       Copyright © SUREKHA TECHNOLOGIES PRIVATE LIMITED, 2020.
#
#	    You can not extend,republish,modify our code,app,theme without our
#       permission.
#
#       You may not and you may not attempt to and you may not assist others
#       to remove, obscure or alter any intellectual property notices on the
#       Software.
#
##############################################################################
{
    'name': 'E-commerce Theme',
    'version': '13.0.0.1',
    'sequence': 102,
    'author': 'Surekha Technologies Pvt. Ltd.',
    'description': "Multi Purpose, Responsive with advance new features in the e-commerce theme.",
    'summary': "Multi Purpose, Responsive with advance new features in the e-commerce theme.",
    'category': 'Theme/Ecommerce',
    'website': 'https://www.surekhatech.com',
    'depends': ['website', 'website_theme_install', 'website_sale', 'mass_mailing_sale', 'website_mass_mailing', 'website_sale_wishlist',
                'website_sale_comparison'],
    'data': [
        'data/ecommerce_mass_mailing_data.xml',
        'views/assets.xml',
        'views/templates.xml',
        'views/st_ecommerce_config.xml',
        'views/st_ecommerce_theme_snippets.xml'
    ],
    'images': [
        'images/ecommerce_theme.png',
        'static/description/ecommerce_screenshot.png'
    ],
    'application': True,
    'price': 49.00,
    'currency': 'EUR',
    'license': 'Other proprietary',
}
