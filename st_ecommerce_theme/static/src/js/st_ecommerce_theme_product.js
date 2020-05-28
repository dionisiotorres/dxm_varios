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
odoo.define('st_ecommerce_theme.product_view', function(require) {
    "use strict";
    var ajax = require('web.ajax');

    /**
     * for display product on list view
     * @param: {Event} event
     */
    $('#list').click(function(event) {
        event.preventDefault();
        $('#grid').removeClass('active');
        $('#list').addClass('active');
        ajax.jsonRpc("/list_view", 'call', {}).then(function() {
            $(document)[0].location.reload();
        });
    });

    /**
     * for display product on grid view
     * @param: {Event} event
     */
    $('#grid').click(function(event) {
        event.preventDefault();
        $('#list').removeClass('active');
        $('#grid').addClass('active');
        ajax.jsonRpc("/grid_view", 'call', {}).then(function() {
            $(document)[0].location.reload();
        });
    });

    $('form.js_product_brands input, form.js_product_brands select').on('change', function(event) {
        if (!event.isDefaultPrevented()) {
            event.preventDefault();
            $(this).closest("form").submit();
        }
    });

});

$(document).ready(function() {

    // add class for list/grid view
    if ($('#products_grid').length > 0) {
        var products_grid_class = $('#products_grid').attr('class');
        $('.productlist-top').addClass(products_grid_class);
    }

});


odoo.define('st_ecommerce_theme.product_page', function(require) {
    "use strict";

    jQuery(document).ready(function() {

        // social-icon on product details page
        $('.fb_product_share').click(function(e) {
            var share_url = window.location.href;
            var popup_url = _.str.sprintf("https://www.facebook.com/sharer/sharer.php?u=%s", encodeURIComponent(share_url));
            window.open(popup_url, 'Share Dialog', 'width=600,height=400');
        });
        $('.tw_product_share').click(function(e) {
            var share_text = "Share product Page";
            var share_url = window.location.href;
            var popup_url = _.str.sprintf("https://twitter.com/intent/tweet?tw_p=tweetbutton&text=%s %s", share_text, share_url);
            window.open(popup_url, 'Share Dialog', 'width=600,height=400');
        });
        $('.li_product_share').click(function(e) {
            var share_text = "Share product Page";
            var share_url = window.location.href;
            var popup_url = _.str.sprintf("http://www.linkedin.com/shareArticle?mini=true&url=%s&title=I am using odoo&summary=%s&source=www.odoo.com", encodeURIComponent(share_url), share_text);
            window.open(popup_url, 'Share Dialog', 'width=600,height=400');
        });

        // display alternatives products on products details page
        var owl = $("#owl-carousel");

        owl.owlCarousel({

            loop: true,
            autoplay: true,
            autoplayTimeout: 3000,
            margin: 10,

            responsiveClass: true,
            responsive: {
                0: {
                    items: 1,
                },
                600: {
                    items: 3,
                },
                1000: {
                    items: 5,
                }
            }

        });
    });

});