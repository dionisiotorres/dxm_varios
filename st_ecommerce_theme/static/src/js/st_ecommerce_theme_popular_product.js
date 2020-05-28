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
odoo.define('st_ecommerce_theme.popular_products', function(require) {
    "use strict";

    var sAnimation = require('website.content.snippets.animation');

    sAnimation.registry.popular_products = sAnimation.Class.extend({
        selector: ".popular_products",

        start: function() {
            var self = this;
            if (self.editableMode) {
                self.$target.empty();
            }
            if (!self.editableMode) {
                return $.ajax({
                    url: '/website/slider/popular_products',
                    method: 'GET',
                    data: {
                        limit: self.$target.attr('data-popular-product-days'),
                    },
                    success: function(data) {
                        self.$target.empty().append(data);
                        $(".popular_products").owlCarousel({
                            navigation: true,
                            pagination: true,
                            loop: true,
                            autoplay: true,
                            nav: true,
                            dots: false,
                            margin: 20,
                            responsive: {
                                0: {
                                    items: 1,
                                },
                                600: {
                                    items: 3,
                                },
                                1000: {
                                    items: 4,
                                },
                                1100: {
                                    items: 5,
                                }
                            }
                        });
                    },
                });
            }
        }
    });

    return {
        DataSlider: sAnimation.registry.popular_products,
    };

});
