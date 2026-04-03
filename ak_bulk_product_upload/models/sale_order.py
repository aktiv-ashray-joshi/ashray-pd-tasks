#Part of Aktiv Software
from odoo import models,fields,api
from markupsafe import Markup
import time 

class SaleOrder(models.Model):
    """
    Inherit Sale Order to add bulk product upload and line merging functionality.
    """
    _inherit = "sale.order"
    _description = "Sale Order"
    
    is_duplicate_lines = fields.Boolean(compute='_compute_has_duplicate_lines',default=False)
    is_merge_email_pending = fields.Boolean(string="Merge Email Pending", default=False, copy=False)

    @api.depends('order_line','order_line.product_id')
    def _compute_has_duplicate_lines(self):
        for record in self:
            product_ids = [line.product_id.id for line in record.order_line]
            record.is_duplicate_lines = len(product_ids) != len(set(product_ids))

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
                import logging
                _logger = logging.getLogger(__name__)
                _logger.info("Order %s: Lines merged for products %s", record.name, merged_products)
                
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
                _logger.info("Order %s: Found notify_partner_ids: %s", record.name, notify_partner_ids.ids)
                if notify_partner_ids:
                    record.is_merge_email_pending = True
                    _logger.info("Order %s: Marked is_merge_email_pending = True", record.name)

        return True

    @api.model
    def _cron_send_merge_notifications(self):
        """
        Send deferred email notifications to partners about merged order lines using a mail template.
        """
        import logging
        _logger = logging.getLogger(__name__)
        
        template = self.env.ref('ak_bulk_product_upload.ak_email_template_merge_order_lines', raise_if_not_found=False)
        if not template:
            _logger.error("Mail template 'ak_bulk_product_upload.ak_email_template_merge_order_lines' not found.")
            return

        pending_orders = self.search([('is_merge_email_pending', '=', True)])
        _logger.info("Cron _cron_send_merge_notifications running. Found %d pending orders.", len(pending_orders))
        
        for order in pending_orders:
            if order.company_id.notify_partner_ids:
                template.send_mail(order.id, force_send=True)
                _logger.info("Sent merge notification email for order %s using template.", order.name)
            order.is_merge_email_pending = False
