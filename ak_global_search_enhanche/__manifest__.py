# -*- coding: utf-8 -*-

{
    "name": "Global Search Enhance",
    "version": "19.0.1.0.0",
    "category": "Tools",
    "summary": "Extend / command palette to search business documents",
    "depends": ["web", "sale", "purchase", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/ak_global_search_rule_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "ak_global_search_enhanche/static/src/command_palette_documents.js",
        ],
    },
    "installable": True,
    "license": "LGPL-3",
}
