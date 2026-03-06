from odoo import models,fields,api,Command

class QuotationBulkUpload(models.TransientModel):
    _name="quotation.bulk.upload"
    _description="Quotation Bulk Upload Product"
    
    sale_order_id = fields.Many2one('sale.order')
    
    line_ids=fields.One2many('quotation.bulk.upload.lines','wizard_id',string="Order Lines")
    
    
    def action_upload(self):
        print("\n\n\n\n>>>>>>>>>>>>>>>Uploaded<<<<<<<<<<<<<<<<<<<<<<<<<<\n\n\n\n")
        # order_lines = self.sale_order_id.order_line
        lines = []
        for line in self.line_ids:
            lines.append(Command.create({
                'product_id' : line.product_id.id,
                'product_uom_qty' : line.quantity,
                'price_unit': line.product_id.lst_price
            }))
        print("\n\n\n\n>>>>>>>>>>>>>>>Uploaded<<<<<<<<<<<<<<<<<<<<<<<<<<\n\n\n\n",lines)
        self.sale_order_id.order_line = lines

        
           
           
           