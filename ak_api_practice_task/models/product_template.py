from odoo import models,fields,api
from odoo.exceptions import ValidationError
import requests
import base64

class PoductTemplate(models.Model):
    _inherit = 'product.template'
    
    external_product_id = fields.Integer(string="Product ID",copy=False)
    
    @api.constrains('external_product_id')
    def _check_external_product_id_unique(self):

        for record in self:

            if record.external_product_id:

                existing_product = self.search([
                    ('external_product_id', '=', record.external_product_id),
                    ('id', '!=', record.id)
                ], limit=1)

                if existing_product:
                    raise ValidationError(
                        "External Product ID must be unique."
                    )
    
    def fetch_external_products(self):
        '''Fetches Products from external System and create records in Odoo'''
        url='https://fakestoreapi.com/products'
        
        response = requests.get(url)
        if response.status_code == 200:
            products = response.json()
            vals_list = []
            for product in products:
            # Prevent Duplication of Records if already exists.
                existing_product_id = self.env['product.template'].search([('external_product_id','=',product['id'])])
                if existing_product_id:
                    continue
            # Check if product categories exists or not , if not create new
                category_id = self.env['product.category'].search([('name','=',product['category'])])
                if not category_id:
                    category_id=self.env['product.category'].create({
                        'name':product['category'],
                    })
                
            # Image Conversion
                image_base64 = False

                image_url = product.get('image')

                if image_url:

                    image_response = requests.get(image_url)

                    if image_response.status_code == 200:
                        image_base64 = base64.b64encode(
                            image_response.content
                        )

                vals={
                    'external_product_id': product['id'],
                    'name': product['title'],
                    'categ_id':category_id.id,
                    'description':product['description'],
                    'list_price':product['price'],
                    'rating_count':product['rating']['count'],
                    'rating_avg':product['rating']['rate'],
                    'image_1920': image_base64,       
                }
                
                vals_list.append(vals)
            return self.env['product.template'].create(vals_list)
        return True           