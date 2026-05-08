#Part of Aktiv Software PVT LTD.
from odoo import models,fields,api
from odoo.exceptions import ValidationError
import requests
class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    external_user_id = fields.Integer(string="User ID",copy=False)
    external_username = fields.Char(string="User Name",copy=False)
    
    @api.constrains('external_user_id')
    def _check_external_user_id_unique(self):
        for record in self:
            if record.external_user_id:
                existing = self.search([
                    ('external_user_id', '=', record.external_user_id),
                    ('id', '!=', record.id)
                ], limit=1)
                if existing:
                    raise ValidationError(
                        "External User ID must be unique."
                    )
    
    def fetch_external_partners(self):
        """Fetches the data of partners from external API and creates in Odoo"""
        url='https://jsonplaceholder.typicode.com/users'
        
        response = requests.get(url)
        
        if response.status_code == 200:
            partners = response.json()
            
            vals_list=[]
            
            for partner in partners:
            # If partner already exits prevent duplicate records creation    
                existing_partner = self.env['res.partner'].search([('external_user_id','=',partner['id'])])
                if existing_partner:
                    continue
            # Check if comapny exits or not , if not create then assign to partner
                company_name = partner['company']['name']
                parent_id = self.env['res.partner'].search([('name','=',company_name),('is_company','=',True)],limit=1)
                if not parent_id:
                    parent_id = self.env['res.partner'].create({
                        'name':company_name,
                        'is_company':True,
                    })
                
                # Create new partner based on data from external API.
                vals = {
                    'is_company' : False,
                    'external_user_id' : partner['id'],
                    'name': partner['name'],
                    'email':partner['email'],
                    'external_username': partner['username'],
                    'street':partner['address']['street'],
                    'street2':partner['address']['suite'],
                    'city':partner['address']['city'],
                    'zip':partner['address']['zipcode'],
                    'partner_longitude':partner['address']['geo']['lng'],
                    'partner_latitude':partner['address']['geo']['lat'],
                    'phone':partner['phone'],
                    'website':partner['website'],
                    'parent_id':parent_id.id,
                }
                vals_list.append(vals)
            return self.env['res.partner'].create(vals_list)
        return True

