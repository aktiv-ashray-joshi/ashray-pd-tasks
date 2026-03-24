{
    "name": "Stock Location in Sale Order",
    "summary": "Allows Dynamic Stock Location Selection based on Available Quantity in Sale Order",
    "description": """Allows Dynamic Stock Location Selection based on Available Quantity in Sale Order""",
    "website": "https://aktivsoftware.com",
    "category": "Sales",
    "version": "19.0.1.0.0",
    "license": "OPL-1",
    # any module necessary for this one to work correctly
    "depends": ['sale_management', 'stock'],
    # always loaded
    "data": [
        "views/sale_order_views.xml"
    ],
    "installable": True,
    "application": True,
    "auto_install": False,

}