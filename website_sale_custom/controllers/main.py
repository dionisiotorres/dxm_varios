# -*- coding: utf-8 -*-


from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleCustom(WebsiteSale):

    @http.route(auth="user")
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        res = super(WebsiteSaleCustom, self).shop(page=page,
                                                    category=category,
                                                    search=search, ppg=ppg,
                                                    **post)
        return res
