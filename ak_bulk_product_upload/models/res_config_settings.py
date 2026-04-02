from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    """
    Inherit Res Config Settings to manage bulk upload notification settings.
    """
    _inherit = 'res.config.settings'

    notify_partner_ids = fields.Many2many(
        related='company_id.notify_partner_ids',
        string="Notify Personals",
        readonly=False
    )

    