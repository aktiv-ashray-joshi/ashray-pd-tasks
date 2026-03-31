from odoo import _, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def copy(self, default=None):
        self.ensure_one()

        if self.state == "sale":
            raise UserError(
                _(
                    "Cannot duplicate a confirmed sale order '%s'. "
                    "Cancelling a confirmed order would affect deliveries and invoices. "
                    "Please cancel it manually before duplicating."
                )
                % self.name
            )

        if self.state == "cancel":
            raise UserError(
                _(
                    "Cannot duplicate the cancelled sale order '%s'. "
                    "Duplicating a cancelled order would result in attempting "
                    "to cancel it again, which would mislead the system."
                )
                % self.name
            )

        new_order = super().copy(default=default)

        attachments = self.env["ir.attachment"].search(
            [
                ("res_model", "=", "sale.order"),
                ("res_id", "=", self.id),
            ]
        )
        for attachment in attachments:
            attachment.copy({"res_id": new_order.id})

        self.action_cancel()

        return new_order
