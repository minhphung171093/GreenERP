# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Project',
    'version' : '1.1',
    'summary': 'Project Manager',
    'sequence': 30,
    'author': 'Pham Huu Tien',
    'description': """
    Project Manager
  """,
    'category' : 'GreenERP',
    'website': 'https://www.odoo.com/page/billing',
    'depends' : ['project'],
    'data': [
             'security/ir.model.access.csv',
             'wizard/green_task_wizard_view.xml',
             'green_project_view.xml',
             
        
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
