# -*- coding: utf-8 -*-


from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleCustom(WebsiteSale):
    
    @http.route(auth="user")
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        return super(WebsiteSaleCustom, self).shop(page=page, category=category, search=search)

    @http.route(auth="user")
    def product(self, product, category='', search='', **kwargs):
        return super(WebsiteSaleCustom, self).product(product, category=category, search=search, **kwargs)

    @http.route(auth="user")
    def cart(self, access_token=None, revive='', **post):
        return super(WebsiteSaleCustom, self).cart(access_token=access_token, revive=revive, **post)

    @http.route(auth="user")
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        return super(WebsiteSaleCustom, self).cart_update(product_id, add_qty=add_qty, set_qty=set_qty, **kw)

    @http.route(auth="user")
    def address(self, **kw):
        return super(WebsiteSaleCustom, self).address(**kw)

    @http.route(auth="user")
    def confirm_order(self, **post):
        return super(WebsiteSaleCustom, self).confirm_order(**post)

    @http.route(auth="user")
    def checkout(self, **post):
        return super(WebsiteSaleCustom, self).checkout(**post)

    @http.route(auth="user")
    def extra_info(self, **post):
        return super(WebsiteSaleCustom, self).extra_info(**post)

    @http.route(auth="user")
    def payment(self, **post):
        return super(WebsiteSaleCustom, self).payment(**post)

    @http.route(auth="user")
    def payment_confirmation(self, **post):
        return super(WebsiteSaleCustom, self).payment_confirmation(**post)
