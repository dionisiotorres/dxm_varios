odoo.define('st_ecommerce_theme.header', function(require) {
    "use strict";

    $(document).ready(function() {
        $('ul#top_menu li[id$="my_cart"]').remove();
        $('.divider').last().nextAll('li').remove();
        $('.divider').last().remove();
    });

});