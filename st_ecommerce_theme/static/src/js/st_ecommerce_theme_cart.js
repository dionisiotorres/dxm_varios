/*###########################################################################
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
#############################################################################*/
odoo.define('st_ecommerce_theme.cart', function(require) {
    "use strict";

    var sAnimations = require('website.content.snippets.animation');
    var core = require('web.core');

    sAnimations.registry.websiteSaleCartLink.include({
        selector: '#ecommerce_cart li a[href$="/shop/cart"]'

        });

});
