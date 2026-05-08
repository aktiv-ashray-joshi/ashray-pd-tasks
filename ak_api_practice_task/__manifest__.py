{
    'name': 'Ak API Practice',
    'version': '19.0.1.0.0',
    'category': 'Customization',
    'summary': '',
    'description': """Fetch data from external system and create records in Odoo""",
    'depends': ['base','web','contacts','base_geolocalize','sale_management','rating'],
    'data': [
        "views/res_partner_views.xml",
        "views/product_template.xml",
        "views/sale_order.xml"
        ],
    'author':'Aktiv Software PVT. LTD.',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}