from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    

    ak_customer_code = fields.Char(string="Customer Code")

    _unique_ak_customer_code = models.Constraint(
        'unique(ak_customer_code)',
        "Customer Code must be unique",
    )

    @api.model
    def _load_pos_data_fields(self, config):
        "Adds the custom field ak_customer_code to the pos data"""
        fields_list = super()._load_pos_data_fields(config)
        fields_list.append('ak_customer_code')
        return fields_list