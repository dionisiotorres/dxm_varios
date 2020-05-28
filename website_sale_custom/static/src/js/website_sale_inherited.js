
odoo.define('website_sale_custom.website_sale_custom', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var wSaleUtils = require('website_sale.utils');
require('website_sale.website_sale');

publicWidget.registry.WebsiteSale.include({
    events: _.extend({}, publicWidget.registry.WebsiteSale.prototype.events, {
        'click a.js_add_cart_update': '_onClickAddCartUpdate'
    }),

    _onClickAddCartUpdate: function (ev) {
        var self = this;
        var $card = $(ev.currentTarget).closest('.card');
        this._rpc({
            route: "/shop/cart/update_json",
            params: {
                product_id: parseInt($card.find('input[name="product_id"]').val()),
                add_qty: parseInt($card.find('input[name="add_qty"]').val())
            },
        }).then(function (data) {
            wSaleUtils.updateCartNavBar(data);
            $card.find('.cart_item_qty').val(data.quantity).html(data.quantity);
        });
    },
});


});
