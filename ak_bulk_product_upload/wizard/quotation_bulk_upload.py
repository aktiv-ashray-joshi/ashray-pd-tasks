from odoo import models,fields,api,Command

class QuotationBulkUpload(models.TransientModel):
    """
    Wizard to bulk upload products to a sale order.
    """
    _name = "quotation.bulk.upload"
    _description = "Quotation Bulk Upload Product"
    
    sale_order_id = fields.Many2one('sale.order')
    
    line_ids=fields.One2many('quotation.bulk.upload.lines','wizard_id',string="Order Lines")
    
    
    def action_upload(self):
        """
        Upload the selected products and quantities to the linked sale order.
        """
        order_line_values = []
        for line_id in self.line_ids:
            order_line_values.append(Command.create({
                'product_id': line_id.product_id.id,
                'product_uom_qty': line_id.quantity,
                'price_unit': line_id.product_id.lst_price
            }))
        self.sale_order_id.order_line = order_line_values

        
           
           
           