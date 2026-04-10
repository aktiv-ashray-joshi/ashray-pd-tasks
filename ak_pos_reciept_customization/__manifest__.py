{
    'name': 'POS Receipt Customization',
    'version': '19.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Customizations in POS Receipt Customer Name and Product Name',
    'description': """
        Customizations in POS Receipt
    """,
    'depends': ['ak_pos_custom_search'],
    'data': [],
    'assets': {
        'point_of_sale._assets_pos': [
            'ak_pos_reciept_customization/static/src/app/receipt_header.xml',
            'ak_pos_reciept_customization/static/src/app/order_line.xml',
        ],
    },
    'author':'Aktiv Software PVT. LTD.',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}