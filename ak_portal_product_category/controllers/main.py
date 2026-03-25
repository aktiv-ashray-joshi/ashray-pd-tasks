from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

class CustomerPortalProductCategory(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        ProductCategory = request.env['product.category']

        if 'product_category_count' in counters:
            values['product_category_count'] = ProductCategory.sudo().search_count([])

        return values

    @http.route(['/my/product_categories', '/my/product_categories/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_product_categories(self, page=1, sortby=None, **kwargs):
        values = self._prepare_portal_layout_values()
        ProductCategory = request.env['product.category']

        domain = []

        searchbar_sortings = {
            'name': {'label': _('Name'), 'order': 'name asc'},
            'sequence': {'label': _('Sequence'), 'order': 'sequence asc'},
        }
        if not sortby:
            sortby = 'name'
        sort_order = searchbar_sortings[sortby]['order']

        total = ProductCategory.sudo().search_count(domain)

        pager = portal_pager(
            url="/my/product_categories",
            url_args={'sortby': sortby},
            total=total,
            page=page,
            step=self._items_per_page
        )

        categories = ProductCategory.sudo().search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'categories': categories,
            'page_name': 'product_category',
            'pager': pager,
            'default_url': '/my/product_categories',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("ak_portal_product_category.portal_my_product_categories", values)

    @http.route(['/my/product_category/<int:category_id>'], type='http', auth="user", website=True)
    def portal_product_category_form(self, category_id, **kw):
        category = request.env['product.category'].sudo().browse(category_id)
        if not category.exists():
            return request.redirect('/my/product_categories')

        values = self._prepare_portal_layout_values()

        # Fetch products in this category
        products = request.env['product.template'].sudo().search([('categ_id', '=', category.id)])

        values.update({
            'category': category,
            'products': products,
            'page_name': 'product_category',
        })
        return request.render('ak_portal_product_category.portal_product_category_form', values)

    @http.route(['/my/product_category/<int:category_id>/remove_category/<int:product_id>'], type='http', auth="user", website=True, methods=['POST'])
    def portal_remove_product_category(self, category_id, product_id, **kw):
        product = request.env['product.template'].sudo().browse(product_id)

        if product.exists():
            product.write({'categ_id': False})

        return request.redirect(f'/my/product_category/{category_id}')
