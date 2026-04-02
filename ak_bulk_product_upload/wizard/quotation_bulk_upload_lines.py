from odoo import models,api,fields

class QuotationBulkUploadLines(models.TransientModel):
    """
    Transient model to represent a line in the bulk product upload wizard.
    """
    _name = "quotation.bulk.upload.lines"
    _description = "Quotation Bulk Upload Lines"
    
    wizard_id = fields.Many2one('quotation.bulk.upload')
    product_id = fields.Many2one('product.product',string="Products")
    quantity = fields.Float(string="Quantity")

    