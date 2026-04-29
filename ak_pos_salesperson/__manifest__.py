{
    'name': 'POS Salesperson',
    'version': '19.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'POS Salesperson',
    'description': """
        POS Salesperson
    """,
    'depends': ['point_of_sale'],
    'data': [
        'views/res_users_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'ak_pos_salesperson/static/src/app/pos_store_patch.js',
            'ak_pos_salesperson/static/src/app/salesperson_list/salesperson_list.xml',
            'ak_pos_salesperson/static/src/app/salesperson_list/salesperson_list.js',
            'ak_pos_salesperson/static/src/app/select_salesperson_button/select_salesperson_button.xml',
            'ak_pos_salesperson/static/src/app/select_salesperson_button/select_salesperson_button.js',
            'ak_pos_salesperson/static/src/app/select_salesperson_button/payment_screen.js',
        ],
    },
    'author':'Aktiv Software PVT. LTD.',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}