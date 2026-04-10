{
    'name': 'Search Order by Log',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Search Sale Orders based on Log notes',
    'description': """
        This module allows users to search Sale Orders
        based on the content of the chatter log notes.
    """,
    'depends': ['sale'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'author':'Aktiv Software PVT. LTD.',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
