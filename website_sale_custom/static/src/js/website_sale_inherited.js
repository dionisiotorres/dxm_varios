
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
        console.log("ON CART UPDATE");
        // Add product specification options
        if ($('#products_grid').length > 0){
            var parent = $(ev.currentTarget).parents('.o_wsale_product_information');
        } else {
            var parent = $(ev.currentTarget).parents('#product_details');
        }

        var spinner_icon = $("<i class=\"fa fa-spinner fa-spin\"/>");
        var link_button = $(ev.currentTarget);
        var link_button_content = $(ev.currentTarget).html();
        let grade = parent.find("select[name='grade']").children("option:selected").val();
        let color = parent.find("select[name='color']").children("option:selected").val();
        let lock_status = parent.find("select[name='lock_status']").children("option:selected").val();
        let logo = parent.find("select[name='logo']").children("option:selected").val();
        let charger = parent.find("select[name='charger']").children("option:selected").val();
        let network_type = parent.find("select[name='network_type']").children("option:selected").val();
        let lang = parent.find("select[name='lang']").children("option:selected").val();
        let applications = parent.find("select[name='applications']").children("option:selected").val();
        console.log("grade: " + grade);
        console.log($(ev.currentTarget));
        var self = this;

        link_button.html(spinner_icon);

        //var $card = $(ev.currentTarget).closest('.card');
        this._rpc({
            route: "/shop/cart/update_json",
            params: {
                product_id: parseInt(parent.find('input[name="product_id"]').val()),
                add_qty: parseInt(parent.find('input[name="add_qty"]').val()),
                grade: grade,
                color: color,
                lock_status: lock_status,
                logo: logo,
                charger: charger,
                network_type: network_type,
                lang: lang,
                applications: applications
            },
        }).then(function (data) {
            wSaleUtils.updateCartNavBar(data);
            link_button.html(link_button_content);
            parent.find('.cart_item_qty').val(data.quantity).html(data.quantity);
        });
    },
});


});
