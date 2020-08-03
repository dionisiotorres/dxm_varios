odoo.define('mobile_device_sale.variant_mixing', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var concurrency = require('web.concurrency');
    var core = require('web.core');
    var utils = require('web.utils');
    var ajax = require('web.ajax');
    var _t = core._t;

    publicWidget.registry.WebsiteSale.include({

        /**
         * Hack to add and remove from cart with json
         *
         * @param {MouseEvent} ev
         */
        onClickAddCartJSON: function (ev) {
            console.log("UPDATING CART FROM INHERITED JS")
            ev.preventDefault();
            var $link = $(ev.currentTarget);
            var $input = $link.closest('.input-group').find("input");
            var min = parseFloat($input.data("min") || 0);
            var max = parseFloat($input.data("max") || Infinity);
            // var max_available = parseFloat($input.prop("max") || 0);
            var previousQty = parseFloat($input.val() || 0, 10);
            var quantity = ($link.has(".fa-minus").length ? -1 : 1) + previousQty;
            var newQty = quantity > min ? (quantity < max ? quantity : max) : min;


            if (newQty !== previousQty) {
                $input.val(newQty).trigger('change');
            }
            return false;
        },

        /**
         * @private
         * @param {Event} ev
         */
        _onChangeCartQuantity: function (ev) {
            console.log("UPDATE QTY INHERITED")

            var $input = $(ev.currentTarget);
            if ($input.data('update_change')) {
                return;
            }
            var value = parseInt($input.val() || 0, 10);
            if (isNaN(value)) {
                value = 1;
            }
            var max = $input.data('max')
            if (value > max){
                value = max
                $input.val(value)
            }
            var $dom = $input.closest('tr');
            // var default_price = parseFloat($dom.find('.text-danger > span.oe_currency_value').text());
            var $dom_optional = $dom.nextUntil(':not(.optional_product.info)');
            var line_id = parseInt($input.data('line-id'), 10);
            var productIDs = [parseInt($input.data('product-id'), 10)];
            this._changeCartQuantity($input, value, $dom_optional, line_id, productIDs);
        },

    })



    /*var VariantMixin = require('sale.VariantMixin');
    console.log(VariantMixin)
    VariantMixin.onClickAddCartJSON = function (ev) {
            ev.preventDefault();
            console.log("UPDATING CART FROM INHERITED JS")
            var $link = $(ev.currentTarget);
            var $input = $link.closest('.input-group').find("input");
            var min = parseFloat($input.data("min") || 0);
            var max = parseFloat($input.data("max") || Infinity);
            var previousQty = parseFloat($input.val() || 0, 10);
            var quantity = ($link.has(".fa-minus").length ? -1 : 1) + previousQty;
            var newQty = quantity > min ? (quantity < max ? quantity : max) : min;

            if (newQty !== previousQty) {
                $input.val(newQty).trigger('change');
            }
            return false;
        }

    return VariantMixin;*/

});