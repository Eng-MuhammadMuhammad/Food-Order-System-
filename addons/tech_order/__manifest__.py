# -*- coding: utf-8 -*-
{
    'name': "Tech Order",

    'summary': """
        Food Order""",

    'description': """

    """,

    'author': "Tala",
    'website': "https://sy.linkedin.com/in/talah-hjaij",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/add_external_item.xml',
        'wizard/feedback_reason.xml',
        'views/meal.xml',
        'views/order.xml',
        'views/meal_ingredient.xml',
        'views/custome_feedback.xml',
        'views/external_item.xml',
        'views/res_partner.xml',
        'views/res_config_settings.xml',
        'data/server_action.xml',
        'data/scheduale_action.xml',
        'data/sequence.xml',
        'report/order_report.xml',

    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
