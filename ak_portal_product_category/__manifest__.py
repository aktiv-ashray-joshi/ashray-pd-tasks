{
    'name': 'Portal Product Category',
    'version': '19.0.1.0.0',
    'category': 'Website/Website',
    'summary': 'Display Product Public Categories in Portal',
    'description': """
        Adds a card for Product Public Categories on the portal home page, 
        with list and form views.
    """,
    'depends': ['portal', 'website_sale'],
    'data': [
        'views/portal_templates.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
