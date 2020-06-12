odoo.define('oct_website_sale.sale', function (require) {
    'use strict';
    var ajax = require('web.ajax');

    $(document).ready(function () {

        /* Handle layout list options */
        $(document).on('click', '.o_wsale_apply_list', function(event) {
            event.preventDefault();
            $('#grid').removeClass('active');
            $('#list').addClass('active');
            // Apply specs filter css
            let specs_filters = $(".oct_filter_wrapper");
            specs_filters.each(function () {
                let add_class = "col-lg-8 col-md-8";
                let remove_class = "col-lg-12 col-md-12";
                specs_filters.removeClass(remove_class);
                specs_filters.addClass(add_class);
                let oct_filters = $(this).find('.oct_filters');
                oct_filters.removeClass('oct_filters_grid_mode');
                oct_filters.addClass('oct_filters_list_mode');
            })
        }); // END LAYOUT LIST OPTIONS

        /* Handle layout grid options */
        $(document).on('click', '.o_wsale_apply_grid', function(event) {
            event.preventDefault();
            $('#list').removeClass('active');
            $('#grid').addClass('active');
            // Apply specs filter css
            let specs_filters = $(".oct_filter_wrapper");
            specs_filters.each(function () {
                let add_class = "col-lg-12 col-md-12";
                let remove_class = "col-lg-8 col-md-8";
                specs_filters.removeClass(remove_class);
                specs_filters.addClass(add_class);
                let oct_filters = $(this).find('.oct_filters');
                oct_filters.removeClass('oct_filters_list_mode');
                oct_filters.addClass('oct_filters_grid_mode');

            })
        }); // END LAYOUT GRID OPTIONS

        /* Filter product brands */
        $(document).on('change', '.js_product_brands',
            function(event) {
            if (!event.isDefaultPrevented()) {
                event.preventDefault();
                $(this).closest("form").submit();
            }
        }); // END FILTER PRODUCT BRANDS

        /* Product specifications handler */
        $(document).on('change', '.oct_grid_variant_selector',function (e) {
            /* select filter values */
            let grade = $(this).find("select[name='grade']").children("option:selected").val();
            let color = $(this).find("select[name='color']").children("option:selected").val();
            let lock_status = $(this).find("select[name='lock_status']").children("option:selected").val();
            let logo = $(this).find("select[name='logo']").children("option:selected").val();
            let charger = $(this).find("select[name='charger']").children("option:selected").val();
            let network_type = $(this).find("select[name='network_type']").children("option:selected").val();
            let lang = $(this).find("select[name='lang']").children("option:selected").val();
            let applications = $(this).find("select[name='applications']").children("option:selected").val();
            // vars on product grid
            if ($('#products_grid').length > 0){
                var parent_container = $(this).parents('.o_wsale_product_information');
                var product_id = parent_container.find('a').data('oe-id');
                var price_container =  parent_container.find('.oe_currency_value');
                var quant_container =  parent_container.find('.oct_product_qty');
                var qty_input = parent_container.find('.input_add_qty');
                var add_to_cart_button = parent_container.find('.js_add_cart_update');
            } else { // vars on product detail
                var parent_container = $(this).parents('#product_details');
                var product_id = $("input[name='product_template_id']").val();
                var price_container =  parent_container.find('.oe_currency_value');
                var quant_container =  parent_container.find('.oct_product_qty');
                var qty_input = $("input[name='add_qty']");
                var add_to_cart_button = $('#add_to_cart_json');
            }


            let spinner = $("<i class=\"fa fa-spinner fa-spin\"/>");

            $(quant_container).html(spinner);

            ajax.jsonRpc('/shop/get_product_info', 'call', {
                product_id: product_id,
                grade: grade,
                color: color,
                lock_status: lock_status,
                logo: logo,
                charger: charger,
                network_type: network_type,
                lang: lang,
                applications: applications
            }).then(function (data) {
            if (data) {
                console.log(data);
                var new_price = data.product_price;
                $(price_container).each(function () {
                    $(this).text(new_price);
                });
                $(quant_container).html(data.product_quants);

                if (data.product_quants > 0){
                    qty_input.prop( "disabled", false );
                    qty_input.attr({'max': data.product_quants});
                    add_to_cart_button.removeClass('oct_hidden_important');
                } else {
                    qty_input.prop( "disabled", true );
                    add_to_cart_button.addClass('oct_hidden_important');
                }

            } else {

            }
        });

        }); // END PRODUCT SPECIFICATIONS HANDLER

        /* Specifications filter toggle visualization handler */
        $(document).on('click', '.oct_filter_title', function(ev){
            var filter_container = $(this).parents('.oct_grid_variant_selector').find('.oct_filters');
            var selector_icon = $(this).parents('.oct_grid_variant_selector').find('.oct_selector_icon');
            $(this).parents('.oct_grid_variant_selector').find('.oct_filters').toggle("slow", function () {
                if (filter_container.is(":visible")){
                    selector_icon.html("<i class=\"fa fa-caret-up\"/>");
                } else {
                    selector_icon.html("<i class=\"fa fa-caret-down\"/>");
                }
            });
        });


        /* Cart specifications lines remove handler */
        $(document).on('click', '.remove_specs_line', function (ev) {
            ev.preventDefault();
            ev.stopPropagation();
            // get line variables
            var action_icon = $(this).find("i");
            var spinner_icon = $("<i class=\"fa fa-spinner fa-spin\"/>");
            var error_icon = $("<i class='fa fa-ban/>'");
            var specs_id =  $(this).data('specs-id');
            var specs_qty =  parseInt($(this).data('specs-qty'));
            var product_row = $("#" + $(this).data('product-row'));
            var product_total_qty_container = product_row.find('.total_product_qty');
            var product_total_qty =  parseInt(product_total_qty_container.text());
            var specs_row =  $(this).closest('tr');
            var order_line_specs_row =  $(this).closest('.order_line_specs_row');
            var cart_table = $("#cart_products");

            // console.log(product_row);
            // console.log(product_total_qty_container);
            // console.log(product_total_qty);
            // console.log(order_line_specs_row);
            // console.log(cart_table);

            action_icon.html(spinner_icon);

            ajax.jsonRpc('/shop/cart/delete_specs', 'call', {
                    specs_id: specs_id,
                    specs_qty: specs_qty
                }).then(function (data) {
                    if (data) {
                        if (data.success === 'true'){
                            specs_row.remove();
                            var new_qty = product_total_qty - specs_qty;

                            console.log("New qty: " + new_qty);

                            if (new_qty > 0){
                                console.log("new qty GT 0");
                                // product_total_qty = new_qty;
                                product_total_qty_container.text(new_qty);
                            } else {
                                console.log("new qty EQ 0");
                                order_line_specs_row.remove();
                                product_row.remove();
                            }

                            // reload window if no more lines in the cart.
                            if (data.remain_lines === 0){
                                // cart_table.remove();
                                window.location.reload();
                            }
                        } else {
                            // show an error message
                            action_icon.html(error_icon);
                        }

                    } else {

                    }
                });

        })

    }) // END DOCUMENT READY

}); // END ODOO DEFINE