from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

class CustomerPortalProductCategory(CustomerPortal):
    """
    Controller for managing product categories in the customer portal.
    """

    def _prepare_home_portal_values(self, counters):
        """
        Prepare values for the portal home page, including product category count.
        """
        values = super()._prepare_home_portal_values(counters)
        ProductCategory = request.env['product.category']

        if 'product_category_count' in counters:
            values['product_category_count'] = ProductCategory.sudo().search_count([])

        return values

    @http.route(['/my/product_categories', '/my/product_categories/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_product_categories(self, page=1, sortby=None, **kwargs):
        """
        Display the list of product categories in the portal.
        """
        values = self._prepare_portal_layout_values()
        ProductCategory = request.env['product.category']
        domain = []

        searchbar_sortings = {
            'name': {'label': _('Name'), 'order': 'name asc'},
            'id': {'label': _('Sequence'), 'order': 'id asc'},
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

        category_ids = ProductCategory.sudo().search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'category_ids': category_ids,
            'page_name': 'product_category',
            'category_id': False,
            'product_id': False,
            'default_url': '/my/product_categories',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("ak_portal_product_category.portal_my_product_categories", values)

    @http.route(['/my/product_category/<int:category_id>'], type='http', auth="user", website=True)
    def portal_product_category_form(self, category_id, **kw):
        """
        Display the details of a specific product category and its products in the portal.
        """
        category_id = request.env['product.category'].sudo().browse(category_id)
        if not category_id.exists():
            return request.redirect('/my/product_categories')

        values = self._prepare_portal_layout_values()

        product_ids = request.env['product.template'].sudo().search([('categ_id', '=', category_id.id),('is_published', '=', True)])

        values.update({
            'category_id': category_id,
            'product_ids': product_ids,
            'product_id': False,        # breadcrumb: no active product on category page
            'page_name': 'product_category',
        })
        return request.render('ak_portal_product_category.portal_product_category_form', values)

    @http.route(['/my/product_category/<int:category_id>/remove_category/<int:product_id>'], type='http', auth="user", website=True, methods=['POST'])
    def portal_remove_product_category(self, category_id, product_id, **kw):
        """
        Remove a product template from its category.
        """
        product_id = request.env['product.template'].sudo().browse(product_id)

        if product_id.exists():
            product_id.write({'categ_id': False})

        return request.redirect(f'/my/product_category/{category_id}')

    @http.route(['/my/product/<int:product_id>'], type='http', auth="user", website=True)
    def portal_product_detail(self, product_id, **kw):
        """
        Display the details of a specific product in the portal.
        Keeps the user inside portal so breadcrumb chain remains intact.
        """
        product = request.env['product.template'].sudo().browse(product_id)
        if not product.exists() or not product.is_published:
            return request.redirect('/my/product_categories')

        values = self._prepare_portal_layout_values()
        values.update({
            'product_id': product,
            'category_id': product.categ_id,  # breadcrumb: drives Level 2 category link
            'page_name': 'product',
        })
        return request.render('ak_portal_product_category.portal_product_detail', values)
