from odoo import models,fields,api,Command,_
from odoo.exceptions import UserError
class QuotationBulkUpload(models.TransientModel):
    """
    Wizard to bulk upload products to a sale order.
    """
    _name = "quotation.bulk.upload"
    _description = "Quotation Bulk Upload Product"
    
    sale_order_id = fields.Many2one('sale.order')   
    product_ids = fields.Many2many('product.product', string="Products", required=True)
    quantity = fields.Float(string="Quantity", default=1.0)
    
    
    def action_upload(self):
        """
        Upload the selected products and quantities to the linked sale order.
        """
        if not self.product_ids:
            raise UserError(_("Cannot Proceed with Zero Products"))
        if self.quantity <= 0:
            raise UserError(_("Quantity cannot be zero or negative"))
        
        order_line_values = []
        for product in self.product_ids:
            order_line_values.append(Command.create({
                'product_id': product.id,
                'product_uom_qty': self.quantity,
                'price_unit': product.lst_price
            }))
        self.sale_order_id.order_line = order_line_values

        
           
           
           