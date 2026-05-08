from odoo import models,fields,api
from odoo.exceptions import ValidationError
import requests

class SaleOrder(models.Model):
    _inherit='sale.order'
    
    external_order_id = fields.Integer(string="Sale Order Id",copy=False)
    
    @api.constrains('external_order_id')
    def _check_external_order_id_unique(self):

        for record in self:

            if record.external_order_id:

                existing_order = self.search([
                    ('external_order_id', '=', record.external_order_id),
                    ('id', '!=', record.id)
                ], limit=1)

                if existing_order:
                    raise ValidationError(
                        "External Order ID must be unique."
                    )

    def fetch_sales_order(self):
        '''Fetches Sales Order from external system and Create records in Odoo'''
        
        url='https://jsonplaceholder.typicode.com/posts'
        
        response = requests.get(url)
        if response.status_code == 200:
            orders = response.json()
            
            vals_list = []
            
            for order in orders:
                existing_order = self.env['sale.order'].search([('name','=',order['title'])])
                if existing_order:
                    continue
                partner_id = self.env['res.partner'].search([('external_user_id','=',order['userId'])])
                if partner_id:
                    vals = {
                        'name':order['title'],
                        'partner_id': partner_id.id,
                        'note':order['body'],
                        'state':'sale',
                        'external_order_id':order['id'],
                    }
                    
                    vals_list.append(vals)
            return self.env['sale.order'].create(vals_list)
        return True
                    