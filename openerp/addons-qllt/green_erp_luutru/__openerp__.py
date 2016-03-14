# -*- coding: utf-8# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'GreenERP Quản Lý Lưu Trú',
    'version': '1.0',
    'category': 'GreenERP',
    'sequence': 1,
    'author': 'minhphung171093@gmail.com',
    'website' : 'http://incomtech.com.vn/',
    'depends': ['green_erp_base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/khach_luutru_wizard_view.xml',
        'wizard/luutru_theo_quocgia_wizard_view.xml',
        'report/khach_luutru_report_view.xml',
        'report/luutru_theo_quocgia_report_view.xml',
        'ql_luutru_view.xml',
        'menu.xml',
    ],
    'css' : [
    ],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: -*-