# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AkGlobalSearchRule(models.Model):
    _name = "ak.global.search.rule"
    _description = "Global Search Rule"
    _order = "sequence, id"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)

    model_id = fields.Many2one("ir.model", required=True, ondelete="cascade")
    field_ids = fields.Many2many(
        "ir.model.fields",
        string="Search Fields",
        domain="[('model_id', '=', model_id), ('store', '=', True), ('ttype', 'in', ('char', 'text', 'many2one'))]",
        required=True,
    )

    @api.onchange("model_id")
    def _onchange_model_id(self):
        if self.model_id:
            self.name = self.model_id.name
        self.field_ids = False

    @api.constrains("model_id", "field_ids")
    def _check_fields_model(self):
        for rule in self:
            if not rule.model_id:
                continue
            invalid_fields = rule.field_ids.filtered(lambda f: f.model_id != rule.model_id)
            if invalid_fields:
                raise ValidationError(
                    "Some selected fields do not belong to the selected model."
                )
