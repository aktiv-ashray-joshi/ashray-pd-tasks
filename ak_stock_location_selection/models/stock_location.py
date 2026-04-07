from odoo import api, fields, models


class StockLocation(models.Model):
    """Extend stock.location to show available quantity in display name and sort by quantity."""
    _inherit = 'stock.location'

    @api.depends_context('show_available_qty', 'product_id')
    def _compute_display_name(self):
        """Append available quantity to location display name when context keys are set.

        Builds from the stored ``complete_name`` field (always clean) rather
        than appending to ``display_name`` which may already carry a cached
        quantity suffix, preventing the ``(10.0) (10.0)`` duplication bug.
        """
        super()._compute_display_name()
        if self.env.context.get('show_available_qty') and self.env.context.get('product_id'):
            product_id = self.env.context.get('product_id')
            if isinstance(product_id, (list, tuple)):
                product_id = product_id[0]

            quants = self.env['stock.quant'].search([
                ('product_id', '=', product_id),
                ('location_id', 'in', self.ids),
            ])
            qty_by_loc = {}
            for q in quants:
                qty_by_loc[q.location_id.id] = (
                    qty_by_loc.get(q.location_id.id, 0.0) + q.available_quantity
                )

            for location in self:
                available_qty = qty_by_loc.get(location.id, 0.0)
                base = location.complete_name or location.name
                location.display_name = f"{base} ({available_qty})"

    @api.model
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        """Sort dropdown results by available quantity (highest first)."""
        res = super().name_search(name, domain, operator, limit)
        if self.env.context.get('show_available_qty') and self.env.context.get('product_id'):
            product_id = self.env.context.get('product_id')
            if isinstance(product_id, (list, tuple)):
                product_id = product_id[0]

            loc_ids = [r[0] for r in res]
            if loc_ids:
                quants = self.env['stock.quant'].search([
                    ('product_id', '=', product_id),
                    ('location_id', 'in', loc_ids),
                ])
                qty_by_loc = {}
                for q in quants:
                    qty_by_loc[q.location_id.id] = (
                        qty_by_loc.get(q.location_id.id, 0.0) + q.available_quantity
                    )
                res.sort(key=lambda r: qty_by_loc.get(r[0], 0.0), reverse=True)
        return res

    @api.model
    def web_search_read(self, domain=None, specification=None, offset=0,
                        limit=None, order=None, count_limit=None):
        """Sort 'Search More' dialog results by available quantity (highest first)."""
        result = super().web_search_read(
            domain, specification, offset=offset, limit=limit,
            order=order, count_limit=count_limit,
        )
        if self.env.context.get('show_available_qty') and self.env.context.get('product_id'):
            product_id = self.env.context.get('product_id')
            if isinstance(product_id, (list, tuple)):
                product_id = product_id[0]

            records = result.get('records', [])
            loc_ids = [r['id'] for r in records if 'id' in r]
            if loc_ids:
                quants = self.env['stock.quant'].search([
                    ('product_id', '=', product_id),
                    ('location_id', 'in', loc_ids),
                ])
                qty_by_loc = {}
                for q in quants:
                    qty_by_loc[q.location_id.id] = (
                        qty_by_loc.get(q.location_id.id, 0.0) + q.available_quantity
                    )
                records.sort(
                    key=lambda r: qty_by_loc.get(r.get('id'), 0.0),
                    reverse=True,
                )
        return result