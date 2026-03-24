from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Computed helper: location ids that have available stock for the selected product.
    # Used as the domain source for location_id so the dropdown only shows
    # locations where qty > 0 for this product.
    available_location_ids = fields.Many2many(
        comodel_name='stock.location',
        compute='_compute_available_location_ids',
        string='Available Locations',
    )

    # The field that the salesperson picks — stores a stock.location record.
    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Source Location',
        domain="[('id', 'in', available_location_ids)]",
        ondelete='set null',
    )

    # Informational field: available qty for the product at the chosen location.
    available_qty_at_location = fields.Float(
        string='Available Qty',
        compute='_compute_available_qty_at_location',
        digits='Product Unit',
        help='Available (unreserved) quantity of this product at the selected source location.',
    )

    # ── compute methods ──────────────────────────────────────────────────────

    @api.depends('product_id')
    def _compute_available_location_ids(self):
        """Find all internal locations that have available stock for the product."""
        for line in self:
            if line.product_id:
                quants = self.env['stock.quant'].search([
                    ('product_id', '=', line.product_id.id),
                    ('location_id.usage', '=', 'internal'),
                ]).filtered(lambda q: q.available_quantity > 0)
                line.available_location_ids = quants.mapped('location_id')
            else:
                line.available_location_ids = self.env['stock.location']

    @api.depends('product_id', 'location_id')
    def _compute_available_qty_at_location(self):
        """Sum available quantity from stock.quant for product + location."""
        for line in self:
            if line.product_id and line.location_id:
                quants = self.env['stock.quant'].search([
                    ('product_id', '=', line.product_id.id),
                    ('location_id', '=', line.location_id.id),
                ])
                line.available_qty_at_location = sum(
                    quants.mapped('available_quantity')
                )
            else:
                line.available_qty_at_location = 0.0

    # ── onchange ─────────────────────────────────────────────────────────────

    @api.onchange('product_id')
    def _onchange_product_id_reset_location(self):
        """Reset location whenever the product changes."""
        self.location_id = False