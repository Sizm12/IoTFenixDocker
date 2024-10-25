# -*- coding: utf-8 -*-
{
    'name': "Fenix Integration",
    'summary': "Integracion de Modulos",
    'description': "Modulo de Dispositivos y Tipos de Dispositivos",
    'author': "Development",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail', 'fleet'],
    'data': [
        #Security
        'security/ir.model.access.csv',
        #Menu
        'views/devices_menu_view.xml',
        'views/security_menu_view.xml',
        #View
        'views/devices_model_view.xml',
        'views/devices_types_model_view.xml',
        'views/rol_model_view.xml',
        'views/views_model_view.xml',
    ],
}