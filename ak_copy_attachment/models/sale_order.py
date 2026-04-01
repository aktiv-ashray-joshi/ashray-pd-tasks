from odoo import _, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    """
    Inherit Sale Order to handle attachment copying and original order cancellation during duplication.
    """
    _inherit = "sale.order"

    def copy(self, default=None):
        """
        Duplicate the sale order, copying its attachments and cancelling the original order.
        :param default: dict: Fields to override during duplication.
        :return: recordset: The newly created sale order.
        """

        if self.state == "sale":
            raise UserError(
                _(
                    "Cannot duplicate a confirmed sale order '%s'. "
                    "Cancelling a confirmed order would affect deliveries and invoices. "
                    "Please cancel it manually before duplicating."
                )
                % self.name
            )
        new_sale_order_id = super().copy(default=default)

        attachment_ids = self.env["ir.attachment"].search(
            [
                ("res_model", "=", "sale.order"),
                ("res_id", "=", self.id),
            ]
        )
        attachment_ids.write({"res_id": new_sale_order_id.id})
        
        if self.state !="cancel":
            self.action_cancel()

        return new_sale_order_id
