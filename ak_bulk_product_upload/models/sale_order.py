#Part of Aktiv Software

from odoo import models,fields,api

class SaleOrder(models.Model):
    _inherit="sale.order"
    _description="Sale Order"
    

    def action_bulk_product_upload(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bulk Upload',
            'res_model': 'quotation.bulk.upload',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_sale_order_id': self.id}
        }

    def action_merge_order_lines(self):
        print("\n\n\n\n>>>>>>>>>>>Merged<<<<<<<<<<<<<<")
        log_lines = []
        for order in self:
            unique_poduct_ids = self.order_line.mapped('product_id')
            for product_id in unique_poduct_ids:
                lines = order.order_line.filtered(lambda l : l.product_id == product_id)
                if len(lines)>1:
                    total_qty = sum(lines.mapped('product_uom_qty'))
                    lines[0].product_uom_qty = total_qty
                    lines[1:].unlink()
                    log_lines.append(f"[{product_id.default_code}] {product_id.name} merged with {total_qty} quantity.")
            if log_lines:
                order.message_post(
                    body="Quotation Merged: " + ", ".join(log_lines),
                    message_type='notification',
                    subtype_xmlid='mail.mt_note'
                )
            notify_partners = order.company_id.notify_partner_ids
            if notify_partners:
                order.message_post(
                    body="Quotation Merged: " + ", ".join(log_lines),
                    message_type='email',
                    subtype_xmlid='mail.mt_comment',
                    partner_ids=notify_partners.ids,
                )
        return True
