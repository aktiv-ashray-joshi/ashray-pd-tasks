from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    

    ak_customer_code = fields.Char(string="Customer Code",placeholder="Enter Customer Code")

    @api.model
    def _load_pos_data_fields(self, config):
        fields_list = super()._load_pos_data_fields(config)
        fields_list.append('ak_customer_code')
        return fields_list