{
    "name": "Bulk Product Upload",
    "summary": "Allows to Add multi products through a single click",
    "description": """Allows to add multi products through the single click and also merge duplicate order lines.""",
    "website": "https://aktivsoftware.com",
    "category": "Sales",
    "version": "19.0.1.0.0",
    "license": "OPL-1",
    # any module necessary for this one to work correctly
    "depends": ['sale_management'],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "views/sale_order_views.xml",
        "wizard/quotation_bulk_upload_views.xml",
    ],
    'author':'Aktiv Software PVT. LTD.',
    "installable": True,
    "application": True,
    "auto_install": False,

}