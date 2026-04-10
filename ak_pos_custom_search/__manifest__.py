{
    'name': 'POS Custom Search',
    'version': '19.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Allows User to Search Customer through a Customer Code in POS Screens',
    'description': """
        Allows User to Search Customer through a Customer Code in POS Screens
    """,
    'depends': ['point_of_sale'],
    'data': [
        'views/res_partner.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'ak_pos_custom_search/static/src/app/models/res_partner.js',
            'ak_pos_custom_search/static/src/app/screens/partner_list.js',
            'ak_pos_custom_search/static/src/app/screens/partner_line.xml',
        ],
    },
    'author':'Aktiv Software PVT. LTD.',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}