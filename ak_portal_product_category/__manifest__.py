{
    'name': 'Portal Product Category',
    'version': '19.0.1.0.0',
    'category': 'Website/Website',
    'summary': 'Display Product Public Categories in Portal',
    'description': """
        Adds a card for Product Public Categories on the portal home page, 
        with list and form views.
    """,
    'depends': ['portal', 'sale_management','product'],
    'data': [
        'views/portal_templates.xml',
        
    ],
    'assets': {
        'web.assets_frontend': [
            'ak_portal_product_category/static/src/js/product_remove_confirm.js',
        ],
    },
    'author':'Aktiv Software PVT. LTD.',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
