{
    'name': 'Inventory Weather Dashboard',
    'version': '1.0',
    'category': 'Inventory',
    'depends': ['stock', 'sale', 'website'],   # ✅ ADD THIS
    'data': [
        'security/ir.model.access.csv',

        'views/weather_dashboard_views.xml',
        'views/stock_warehouse_views.xml',

        'views/sale_order_views.xml',        # ✅ NEW
        'views/payment_templates.xml',       # ✅ NEW
    ],
    'installable': True,
    'application': True,
}