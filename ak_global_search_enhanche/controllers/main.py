# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class AkGlobalSearchRulesController(http.Controller):
    @http.route("/ak_global_search_enhanche/rules", type="json", auth="user")
    def get_rules(self):
        Rule = request.env["ak.global.search.rule"].sudo()
        rules = Rule.search([("active", "=", True)], order="sequence, id")
        return [
            {
                "id": rule.id,
                "name": rule.name,
                "sequence": rule.sequence,
                "model": rule.model_id.model,
                "fields": rule.field_ids.mapped("name"),
            }
            for rule in rules
            if rule.model_id and rule.field_ids
        ]

