from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    category_section_id = fields.Many2one(
        comodel_name="product.category",
        string="Category Section",
        index=True,
        help="Technical field used by ak_groupby_so_lines to identify section lines created for a product category.",
    )
