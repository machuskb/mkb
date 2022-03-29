# -*- coding: utf-8 -*-
{
    'name': "Odoo Saas Sale Order to Project Task",
    'summary': """
        Este Módulo crea una tarea en el proyecto designado cuando una órden de venta es confirmada.
        """,
    'author': "InuX",
    'website': "https://github.com/fmanime",
    'category': 'sales',
    'version': '14.0',
    'depends': ['project', 'sale', 'base_automation'],
    'data': [
        'data/base_automation_data.xml'
    ],
}
