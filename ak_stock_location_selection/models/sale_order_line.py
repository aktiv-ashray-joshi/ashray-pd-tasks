from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    available_location_ids = fields.Many2many(
        comodel_name='stock.location',
        compute='_compute_available_location_ids',
        string='Available Locations',
    )

    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Source Location',
        domain="[('id', 'in', available_location_ids)]",
        ondelete='set null',
    )

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

    @api.onchange('product_id')
    def _onchange_product_id_reset_location(self):
        """Reset location whenever the product changes."""
        self.location_id = False

    @api.readonly
    def web_read(self, specification):
        """Inject product context into location_id spec so display_name shows quantity.

        The XML view ``context`` on the field is only evaluated by the JS client
        during edit-mode interactions (name_search).  For readonly/saved form
        loads, ``web_read`` does not receive the dynamic context automatically.
        We inject it here so that the base ``web_read`` applies it when
        computing ``display_name`` on the stock.location co-records.
        """
        product_ids_by_line = {}
        needs_fixup = False

        if 'location_id' in specification:
            spec = specification['location_id']
            spec.setdefault('fields', {}).setdefault('display_name', {})

            for line in self:
                if line.product_id and line.location_id:
                    product_ids_by_line[line.id] = line.product_id.id

            unique_pids = set(product_ids_by_line.values())
            if len(unique_pids) == 1:
                spec['context'] = {
                    'show_available_qty': True,
                    'product_id': unique_pids.pop(),
                }
            elif unique_pids:
                needs_fixup = True

        result = super().web_read(specification)

        if needs_fixup:
            for rec_vals in result:
                loc_data = rec_vals.get('location_id')
                if not loc_data or not isinstance(loc_data, dict):
                    continue
                pid = product_ids_by_line.get(rec_vals.get('id'))
                if pid:
                    loc = self.env['stock.location'].with_context(
                        show_available_qty=True, product_id=pid,
                    ).browse(loc_data['id'])
                    loc_data['display_name'] = loc.display_name

        return result