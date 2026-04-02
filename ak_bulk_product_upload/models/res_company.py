from odoo import models, fields

class ResCompany(models.Model):
    """
    Inherit Res Company to add notification partners for bulk upload.
    """
    _inherit = 'res.company'
    
    notify_partner_ids = fields.Many2many(
        'res.partner',
        string="Notify Personals"
    )
