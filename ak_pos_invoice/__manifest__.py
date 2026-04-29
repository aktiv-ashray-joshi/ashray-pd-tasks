{
    'name': 'POS Receipt Customization - Invoice Number',
    'version': '19.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Customizations in POS Receipt - Invoice Number',
    'description': """
        Customizations in POS Receipt
    """,
    'depends': ['point_of_sale'],
    'data': [],
    'assets': {
        'point_of_sale._assets_pos': [
            'ak_pos_invoice/static/src/app/receipt_header.xml',
        ],
    },
    'author':'Aktiv Software PVT. LTD.',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}