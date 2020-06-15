from odoo.http import request
from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.exceptions import ValidationError
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.osv import expression
from odoo.addons.website_sale.controllers.main import WebsiteSale
from werkzeug.exceptions import Forbidden, NotFound
import datetime
import logging

_logger = logging.getLogger(__name__)


class TableCompute(object):

    def __init__(self):
        self.table = {}

    def _check_place(self, posx, posy, sizex, sizey, ppr):
        res = True
        for y in range(sizey):
            for x in range(sizex):
                if posx + x >= ppr:
                    res = False
                    break
                row = self.table.setdefault(posy + y, {})
                if row.setdefault(posx + x) is not None:
                    res = False
                    break
            for x in range(ppr):
                self.table[posy + y].setdefault(x, None)
        return res

    def process(self, products, ppg=20, ppr=4):
        # Compute products positions on the grid
        minpos = 0
        index = 0
        maxy = 0
        x = 0
        for p in products:
            x = min(max(p.website_size_x, 1), ppr)
            y = min(max(p.website_size_y, 1), ppr)
            if index >= ppg:
                x = y = 1

            pos = minpos
            while not self._check_place(pos % ppr, pos // ppr, x, y, ppr):
                pos += 1
            # if 21st products (index 20) and the last line is full (ppr products in it), break
            # (pos + 1.0) / ppr is the line where the product would be inserted
            # maxy is the number of existing lines
            # + 1.0 is because pos begins at 0, thus pos 20 is actually the 21st block
            # and to force python to not round the division operation
            if index >= ppg and ((pos + 1.0) // ppr) > maxy:
                break

            if x == 1 and y == 1:   # simple heuristic for CPU optimization
                minpos = pos // ppr

            for y2 in range(y):
                for x2 in range(x):
                    self.table[(pos // ppr) + y2][(pos % ppr) + x2] = False
            self.table[pos // ppr][pos % ppr] = {
                'product': p, 'x': x, 'y': y,
                'class': " ".join(x.html_class for x in p.website_style_ids if x.html_class)
            }
            if index <= ppg:
                maxy = max(maxy, y + (pos // ppr))
            index += 1

        # Format table according to HTML needs
        rows = sorted(self.table.items())
        rows = [r[1] for r in rows]
        for col in range(len(rows)):
            cols = sorted(rows[col].items())
            x += len(cols)
            rows[col] = [r[1] for r in cols if r[1]]

        return rows


class WebsiteSale(WebsiteSale):

    def sitemap_shop(env, rule, qs):
        if not qs or qs.lower() in '/shop':
            yield {'loc': '/shop'}

        Category = env['product.public.category']
        dom = sitemap_qs2dom(qs, '/shop/category', Category._rec_name)
        dom += env['website'].get_current_website().website_domain()
        for cat in Category.search(dom):
            loc = '/shop/category/%s' % slug(cat)
            if not qs or qs.lower() in loc:
                yield {'loc': loc}

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True, sitemap=sitemap_shop)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        _logger.info("ON SHOP INHERITED CONTROLLER")
        add_qty = int(post.get('add_qty', 1))
        Category = request.env['product.public.category']
        if category:
            category = Category.search([('id', '=', int(category))], limit=1)
            if not category or not category.can_access_from_current_website():
                raise NotFound()
        else:
            category = Category

        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        domain = self._get_search_domain(search, category, attrib_values)

        keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list, order=post.get('order'))

        pricelist_context, pricelist = self._get_pricelist_context()

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        url = "/shop"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        Product = request.env['product.template'].with_context(bin_size=True)

        search_product = Product.search(domain)
        website_domain = request.website.website_domain()
        categs_domain = [('parent_id', '=', False)] + website_domain
        if search:
            search_categories = Category.search([('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
            categs_domain.append(('id', 'in', search_categories.ids))
        else:
            search_categories = Category
        categs = Category.search(categs_domain)

        if category:
            url = "/shop/category/%s" % slug(category)

        product_count = len(search_product)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        products = Product.search(domain, limit=ppg, offset=pager['offset'], order=self._get_search_order(post))

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            attributes = ProductAttribute.search([('product_tmpl_ids', 'in', search_product.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        layout_mode = request.session.get('website_sale_shop_layout_mode')
        if not layout_mode:
            if request.website.viewref('website_sale.products_list_view').active:
                layout_mode = 'list'
            else:
                layout_mode = 'grid'
        # Specs values
        grades = request.env['x_grado'].sudo().search([])
        device_colors = request.env['x_color'].sudo().search([])
        device_lock_status = request.env['x_bloqueo'].sudo().search([])
        device_logo = request.env['x_logo'].sudo().search([])
        device_charger = request.env['x_cargador'].sudo().search([])
        device_network_type = request.env['x_red'].sudo().search([])
        device_lang = request.env['x_idioma_terminal'].sudo().search([])
        device_applications = request.env['x_terminal_aplicaciones'].sudo().search([])

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'add_qty': add_qty,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg, ppr),
            'ppg': ppg,
            'ppr': ppr,
            'categories': categs,
            'attributes': attributes,
            'keep': keep,
            'search_categories_ids': search_categories.ids,
            'layout_mode': layout_mode,
            'grades': grades,
            'device_colors': device_colors,
            'device_lock_status': device_lock_status,
            'device_logo': device_logo,
            'device_charger': device_charger,
            'device_network_type': device_network_type,
            'device_lang': device_lang,
            'device_applications': device_applications
        }
        if category:
            values['main_object'] = category
        return request.render("website_sale.products", values)

    @http.route(['''/shop/get_product_info'''], type='json', auth="user", website=True)
    def get_product_info(self, product_id=None, grade=None, color=0, lock_status=0, logo=0, charger=0,
                         network_type=0, lang=0, applications=0):
        product_obj = request.env['product.template'].browse(int(product_id))
        pricelist = self._get_pricelist_context()[1].id
        pricelist_obj = request.env['product.pricelist'].browse(int(pricelist))
        partner_id = request.env.user.partner_id
        partner_price_list = partner_id.property_product_pricelist
        if partner_price_list:
            pricelist_obj = partner_price_list
        today = datetime.date.today()
        product_price = pricelist_obj.get_product_price(product_obj, 1, partner_id, grade=int(grade), date=today)
        product_quants = self.get_product_quants(product_obj.product_variant_id,
                                                 grade=int(grade),
                                                 color=int(color),
                                                 lock_status=int(lock_status),
                                                 logo=int(logo),
                                                 charger=int(charger),
                                                 network_type=int(network_type),
                                                 lang=int(lang),
                                                 applications=int(applications))

        return {'product_id': product_id, 'pricelist': pricelist_obj.id, 'product_price': product_price,
                'product_quants': product_quants}

    def get_product_quants(self, product_id, **kwargs):
        company_id = request.env.user.company_id
        warehouse_id = request.env['stock.warehouse'].search([('company_id', '=', company_id.id)])
        stock_location = warehouse_id.lot_stock_id
        all_product_quants = request.env['stock.quant']._gather(product_id, stock_location)
        lot_filter = ''
        operand = " and "
        # grade
        if 'grade' in kwargs.keys():
            if kwargs.get('grade') != 0:
                lot_filter = 'q.lot_id.x_studio_revision_grado.id == %s' % kwargs.get('grade')
        # Color
        if 'color' in kwargs.keys():
            if len(lot_filter) > 0 and kwargs.get('color') != 0:
                lot_filter += operand + "q.lot_id.x_studio_color.id == %s" % kwargs.get('color')
            elif kwargs.get('color') != 0:
                lot_filter = "q.lot_id.x_studio_color.id == %s" % kwargs.get('color')
        # Lock Status
        if 'lock_status' in kwargs.keys():
            if len(lot_filter) > 0 and kwargs.get('lock_status') != 0:
                lot_filter += operand + "q.lot_id.x_studio_bloqueo.id == %s" % kwargs.get('lock_status')
            elif kwargs.get('lock_status') != 0:
                lot_filter = "q.lot_id.x_studio_bloqueo.id == %s" % kwargs.get('lock_status')

        # Logo
        if 'logo' in kwargs.keys():
            if len(lot_filter) > 0 and kwargs.get('logo') != 0:
                lot_filter += operand + "q.lot_id.x_studio_logo.id == %s" % kwargs.get('logo')
            elif kwargs.get('logo') != 0:
                lot_filter = "q.lot_id.x_studio_logo.id == %s" % kwargs.get('logo')

        # Charger
        if 'charger' in kwargs.keys():
            if len(lot_filter) > 0 and kwargs.get('charger') != 0:
                lot_filter += operand + "q.lot_id.x_studio_cargador.id == %s" % kwargs.get('charger')
            elif kwargs.get('charger') != 0:
                lot_filter = "q.lot_id.x_studio_cargador.id == %s" % kwargs.get('charger')

        # Network Type
        if 'network_type' in kwargs.keys():
            if len(lot_filter) > 0 and kwargs.get('network_type') != 0:
                lot_filter += operand + "q.lot_id.x_studio_red.id == %s" % kwargs.get('network_type')
            elif kwargs.get('network_type') != 0:
                lot_filter = "q.lot_id.x_studio_red.id == %s" % kwargs.get('network_type')

        # Lang
        if 'lang' in kwargs.keys():
            if len(lot_filter) > 0 and kwargs.get('lang') != 0:
                lot_filter += operand + "q.lot_id.x_studio_idioma.id == %s" % kwargs.get('lang')
            elif kwargs.get('lang') != 0:
                lot_filter = "q.lot_id.x_studio_idioma.id == %s" % kwargs.get('lang')

        # Applications
        if 'applications' in kwargs.keys():
            if len(lot_filter) > 0 and kwargs.get('applications') != 0:
                lot_filter += operand + "q.lot_id.x_studio_aplicaciones.id == %s" % kwargs.get('applications')
            elif kwargs.get('applications') != 0:
                lot_filter = "q.lot_id.x_studio_aplicaciones.id == %s" % kwargs.get('applications')

        if len(lot_filter) > 0:
            quants_filtered = all_product_quants.filtered(lambda q: eval(lot_filter))
        else:
            quants_filtered = all_product_quants

        return len(quants_filtered)

    @http.route(['/shop/cart/update_json'], type='json', auth="user", methods=['POST'], website=True, csrf=False)
    def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True, **kwargs):
        """This route is called when changing quantity from the cart or adding
        a product from the wishlist."""
        _logger.info("!!!!!UPDATING CART VIA JSON INHERITED.....")
        _logger.info("PROCESSING PRODUCT ID: %r", product_id)
        _logger.info("PROCESSING LINE ID: %r", line_id)
        _logger.info("PROCESSING ADD QTY: %r", add_qty)
        _logger.info("PROCESSING SET QTY: %r", set_qty)
        _logger.info("PROCESSING KEYWORD ARGS: %r", kwargs)
        order = request.website.sale_get_order(force_create=1, **kwargs)
        if order.state != 'draft':
            request.website.sale_reset()
            return {}

        value = order._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty, **kwargs)

        if not order.cart_quantity:
            request.website.sale_reset()
            return value

        order = request.website.sale_get_order(**kwargs)
        value['cart_quantity'] = order.cart_quantity

        if not display:
            return value

        value['website_sale.cart_lines'] = request.env['ir.ui.view'].render_template("website_sale.cart_lines", {
            'website_sale_order': order,
            'date': fields.Date.today(),
            'suggested_products': order._cart_accessories()
        })
        value['website_sale.short_cart_summary'] = request.env['ir.ui.view'].render_template(
            "website_sale.short_cart_summary", {
                'website_sale_order': order,
            })
        _logger.info("VALUE AT _CART_UPDATE_JSON: %r", value)
        return value

    def _prepare_product_values(self, product, category, search, **kwargs):
        add_qty = int(kwargs.get('add_qty', 1))

        product_context = dict(request.env.context, quantity=add_qty,
                               active_id=product.id,
                               partner=request.env.user.partner_id)
        ProductCategory = request.env['product.public.category']

        if category:
            category = ProductCategory.browse(int(category)).exists()

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attrib_set = {v[1] for v in attrib_values}

        keep = QueryURL('/shop', category=category and category.id, search=search, attrib=attrib_list)

        categs = ProductCategory.search([('parent_id', '=', False)])

        pricelist = request.website.get_current_pricelist()

        if not product_context.get('pricelist'):
            product_context['pricelist'] = pricelist.id
            product = product.with_context(product_context)

        # Needed to trigger the recently viewed product rpc
        view_track = request.website.viewref("website_sale.product").track

        grades = request.env['x_grado'].search([])
        device_colors = request.env['x_color'].search([])
        device_lock_status = request.env['x_bloqueo'].search([])
        device_logo = request.env['x_logo'].search([])
        device_charger = request.env['x_cargador'].search([])
        device_network_type = request.env['x_red'].search([])
        device_lang = request.env['x_idioma_terminal'].search([])
        device_applications = request.env['x_terminal_aplicaciones'].search([])

        return {
            'search': search,
            'category': category,
            'pricelist': pricelist,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'keep': keep,
            'categories': categs,
            'main_object': product,
            'product': product,
            'add_qty': add_qty,
            'view_track': view_track,
            'grades': grades,
            'device_colors': device_colors,
            'device_lock_status': device_lock_status,
            'device_logo': device_logo,
            'device_charger': device_charger,
            'device_network_type': device_network_type,
            'device_lang': device_lang,
            'device_applications': device_applications
        }

    @http.route(['/shop/cart/delete_specs'], type='json', auth="user", methods=['POST'], website=True, csrf=False)
    def cart_update_specs(self, specs_id, **kwargs):
        """This route is called when delete sale order line specifications."""
        _logger.info("!!!!!DELETING SPECS ID: %r", specs_id)
        specs_obj = request.env['product.line.specs'].sudo().search([('id', '=', int(specs_id))])
        remain_order_lines = 0
        if specs_obj:
            line_obj = specs_obj.sale_order_line_id
            sale_obj = line_obj.order_id
            new_line_qty = line_obj.product_uom_qty - specs_obj.quantity
            specs_obj.unlink()
            if new_line_qty > 0:
                line_obj.write({'product_uom_qty': new_line_qty})
            else:
                line_obj.unlink()
            remain_order_lines = len(sale_obj.order_line)

        result = {
            'remain_lines': remain_order_lines,
            'success': 'true'
        }
        return result
