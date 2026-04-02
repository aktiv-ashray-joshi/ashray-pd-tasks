#Part of Aktiv Software

from odoo import models,fields,api
from markupsafe import Markup
class SaleOrder(models.Model):
    """
    Inherit Sale Order to add bulk product upload and line merging functionality.
    """
    _inherit = "sale.order"
    _description = "Sale Order"
    

    def action_bulk_product_upload(self):
        """
        Open the bulk product upload wizard.
        :return: dict: Window action to open the wizard.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bulk Upload',
            'res_model': 'quotation.bulk.upload',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_sale_order_id': self.id}
        }

    def action_merge_order_lines(self):
        """
        Merge duplicate order lines for the same product into a single line.
        """

        for record in self:
            merged_products = []
            unique_product_ids = record.order_line.mapped('product_id')

            for product_id in unique_product_ids:
                line_ids = record.order_line.filtered(lambda l: l.product_id == product_id)
                if len(line_ids) > 1:
                    total_qty = sum(line_ids.mapped('product_uom_qty'))
                    updated_unit_price = sum(line_ids.mapped('price_subtotal')) / total_qty
                    line_ids[0].product_uom_qty = total_qty
                    line_ids[0].price_unit = updated_unit_price
                    line_ids[1:].unlink()
                    merged_products.append(product_id.name)

            if merged_products:
                product_list = "".join(f"<li>{p}</li>" for p in merged_products)
                body = Markup(f"""
                    <p>Order lines have been merged in Quotation <strong>{record.name}</strong>.</p>
                    <p>Merged Products:</p>
                    <ul>{product_list}</ul>
                """)
                record.message_post(
                    body=body,
                    message_type='notification',
                    subtype_xmlid='mail.mt_note',
                )
                notify_partner_ids = record.company_id.notify_partner_ids
                if notify_partner_ids:
                    record.message_post(
                        body=body,
                        message_type='email',
                        subtype_xmlid='mail.mt_comment',
                        partner_ids=notify_partner_ids.ids,
                    )
        return True