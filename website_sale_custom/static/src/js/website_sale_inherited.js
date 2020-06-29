
odoo.define('website_sale_custom.website_sale_custom', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var wSaleUtils = require('website_sale.utils');
require('website_sale.website_sale');
var Dialog = require('web.Dialog');
var core = require('web.core');
var _t = core._t;

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
        var max_qty_input = parseInt(parent.find('input[name="add_qty"]').prop('max'));
        var qty_input = parseInt(parent.find('input[name="add_qty"]').val());
        let grade = parent.find("input:radio[name=optradio]:checked").val();
        let color = parent.find("input:radio[name=color]:checked").val();
        /*let lock_status = parent.find("select[name='lock_status']").children("option:selected").val();
        let logo = parent.find("select[name='logo']").children("option:selected").val();
        let charger = parent.find("select[name='charger']").children("option:selected").val();
        let network_type = parent.find("select[name='network_type']").children("option:selected").val();
        let lang = parent.find("select[name='lang']").children("option:selected").val();
        let applications = parent.find("select[name='applications']").children("option:selected").val();*/
        console.log("grade: " + grade);
        // console.log($(ev.currentTarget));
        var self = this;

        link_button.html(spinner_icon);

        //var $card = $(ev.currentTarget).closest('.card');

        if (grade && color){

            if (qty_input <= max_qty_input){
                this._rpc({
                    route: "/shop/cart/update_json",
                    params: {
                        product_id: parseInt(parent.find('input[name="product_id"]').val()),
                        add_qty: qty_input,
                        grade: grade,
                        color: color
                    },
                    }).then(function (data) {
                        wSaleUtils.updateCartNavBar(data);
                        link_button.html(link_button_content);
                        parent.find('.cart_item_qty').val(data.quantity).html(data.quantity);
                    });

            } else {
                var dialog = new Dialog(this, {
                size: 'medium',
                dialogClass: 'o_act_window',
                title: _t("Quantity mismatch"),
                $content: $(_t("<span class='text-center' style='padding: 2rem;'>Product quantity can't be greater than available stock quantity.</span>"))
                });
                dialog.open();
                link_button.html(link_button_content);
            }


        } else {
            var dialog = new Dialog(this, {
                size: 'medium',
                dialogClass: 'o_act_window',
                title: _t("Missing Requirements"),
                $content: $(_t("<span class='text-center' style='padding: 2rem;'>Please, select grade and color to add this product to your cart.</span>"))
            });
            dialog.open();
            link_button.html(link_button_content);

        }

    },
});


});
