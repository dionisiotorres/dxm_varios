/*############################################################################
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
##############################################################################*/
odoo.define('st_ecommerce_theme.editor', function(require) {
    'use strict';

    var options = require('web_editor.snippets.options');

    options.registry.popular_products_option_type = options.Class.extend({
        start: function() {
            return this._super.apply(this, arguments);
        },

        limit_product: function(previewMode, value) {
            $('.popular_products').attr("data-popular-product-days", value);
        },

    });

});