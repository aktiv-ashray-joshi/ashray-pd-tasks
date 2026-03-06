from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    notify_partner_ids = fields.Many2many('res.partner', string="Notify Personals")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    notify_partner_ids = fields.Many2many(
        related='company_id.notify_partner_ids',
        string="Notify Personals",
        readonly=False
    )

    