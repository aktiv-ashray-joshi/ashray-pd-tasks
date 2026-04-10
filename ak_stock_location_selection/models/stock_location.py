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
    def search_fetch(self,domain,field_names=None,offset=0,limit=None,order=None):
        """Sort Search More results by available quantity (highest first)."""
        # First call base method
        res = super().search_fetch(
            domain,
            field_names=field_names,
            offset=offset,
            limit=limit,
            order=order,
        )

        # Apply custom sorting
        if (
            self.env.context.get('show_available_qty')
            and self.env.context.get('product_id')
            and res
        ):
            product_id = self.env.context.get('product_id')

            if isinstance(product_id, (list, tuple)):
                product_id = product_id[0]

            loc_ids = res.ids

            if loc_ids:
                quants = self.env['stock.quant'].search([
                    ('product_id', '=', product_id),
                    ('location_id', 'in', loc_ids),
                ])

                qty_by_loc = {}

                for q in quants:
                    qty_by_loc[q.location_id.id] = (
                        qty_by_loc.get(q.location_id.id, 0.0)
                        + q.available_quantity
                    )

                # Sort recordset
                res = res.sorted(
                    key=lambda r: qty_by_loc.get(r.id, 0.0),
                    reverse=True,
                )

        # Return result
        return res