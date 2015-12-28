{
    'name': 'GreenERP Website Sale',
    'category': 'GreenERP',
    'version': '1.0',
    'description': """

        """,
    'author': 'Phung Pham',
    'depends': ['website_partner', 'sale', 'website_mail'],
    'data': [
        'data/config_data.xml',
        'views/green_erp_sale_views.xml',
        'views/templates.xml',
    ],
    'installable': True,
}
