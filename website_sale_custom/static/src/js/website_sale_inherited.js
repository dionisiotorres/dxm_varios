
odoo.define('website_sale_custom.website_sale_custom', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var wSaleUtils = require('website_sale.utils');
var ajax = require('web.ajax');
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

        var website_id = $("html").data('website-id') | 0;
        ajax.jsonRpc('/shop/get_mobile_device_sell_website', 'call', {}).then(function (data) {
            console.log(data);

            var spinner_icon = $("<i class=\"fa fa-spinner fa-spin\"/>");
            var link_button = $(ev.currentTarget);
            var link_button_content = $(ev.currentTarget).html();
            var max_qty_input = parseInt(parent.find('input[name="add_qty"]').prop('max'));
            var qty_input = parseInt(parent.find('input[name="add_qty"]').val());

            var self = this;

            var website_for_sell = data.website_mobile_sell;

            link_button.html(spinner_icon);

            if (website_for_sell === website_id) { // On website 1



                let grade = parent.find("input:radio[name=optradio]:checked").val();
                let color = parent.find("input:radio[name=color]:checked").val();
                let specs = parent.find('.specs_selected').data('specs');
                /*let lock_status = parent.find("select[name='lock_status']").children("option:selected").val();
                let logo = parent.find("select[name='logo']").children("option:selected").val();
                let charger = parent.find("select[name='charger']").children("option:selected").val();
                let network_type = parent.find("select[name='network_type']").children("option:selected").val();
                let lang = parent.find("select[name='lang']").children("option:selected").val();
                let applications = parent.find("select[name='applications']").children("option:selected").val();*/
                console.log("grade: " + grade);
                // console.log($(ev.currentTarget));




                //var $card = $(ev.currentTarget).closest('.card');

                if (grade && color){

                    if (qty_input <= max_qty_input){
                        ajax.jsonRpc("/shop/cart/update_json", 'call', {
                                product_id: parseInt(parent.find('input[name="product_id"]').val()),
                                add_qty: qty_input,
                                grade: grade,
                                color: color,
                                specs: specs
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




            } else {  // On website 2



                // if (qty_input <= max_qty_input){
                    ajax.jsonRpc("/shop/cart/update_json", 'call', {
                            product_id: parseInt(parent.find('input[name="product_id"]').val()),
                            add_qty: qty_input
                        }).then(function (data) {
                            wSaleUtils.updateCartNavBar(data);
                            link_button.html(link_button_content);
                            parent.find('.cart_item_qty').val(data.quantity).html(data.quantity);
                        });

                /*} else {
                    var dialog = new Dialog(this, {
                    size: 'medium',
                    dialogClass: 'o_act_window',
                    title: _t("Quantity mismatch"),
                    $content: $(_t("<span class='text-center' style='padding: 2rem;'>Product quantity can't be greater than available stock quantity.</span>"))
                    });
                    dialog.open();
                    link_button.html(link_button_content);
                }
*/






            }

        });


    },
});


});
