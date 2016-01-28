# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2010-2012 OpenERP SA (<http://openerp.com>).
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

from openerp.osv import osv, fields
from openerp.tools.translate import _
import time

class green_erp_voucher(osv.osv):
    _name = "green.erp.voucher"
    _order = 'date desc'
    def _get_ngay_str(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.date or False
        return res

    _columns = {
        'name': fields.char('Số', size=1024),
        'user_id': fields.many2one('res.users', 'Nhân viên'),
        'date': fields.date('Ngày'),
        'date_str': fields.function(_get_ngay_str, type='char', string='Ngày', store=True),
        'project_id': fields.many2one('du.an', 'Dự án'),
        'noi_dung': fields.text('Nội dung'),
        'hang_muc_id': fields.many2one('hang.muc', 'Hạng mục'),
        'thanh_tien': fields.float('Thành tiền'),
        'company_id': fields.many2one('res.company', 'Công ty'),
        'phuongthuc_thanhtoan_id': fields.many2one('phuongthuc.thanhtoan', 'Nguồn tài chính'),
        'type': fields.selection([('thuc_thu','Thực thu'),('thuc_chi','Thực chi'),('du_thu','Dự thu'),('du_chi','Dự chi')], 'Loại'),
        'ghi_chu': fields.text('Ghi chú'),
        'giai_doan_id': fields.many2one('giai.doan', 'Giai đoạn'),
    }
    
    def _get_company(self, cr, uid, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid)
        return user.company_id and user.company_id.id or False
    
    _defaults = {
        'user_id': lambda self, cr, uid, context=None: uid,
        'company_id': _get_company,
        'date': time.strftime('%Y-%m-%d'),
        'name': '/',
        'thanh_tien': 0,
    }
    
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if vals.get('name', '/') == '/' or 'name' not in vals:
            vals['name'] = self.pool.get('ir.sequence').get(cr, 1, 'greenerp_thuchi', context=context) or '/'
        return super(green_erp_voucher, self).create(cr, uid, vals, context)
    
green_erp_voucher()

class du_an(osv.osv):
    _name = "du.an"
    
    _columns = {
        'name': fields.char('Tên', size=1024, required=True),
    }
    
du_an()

class hang_muc(osv.osv):
    _name = "hang.muc"
    
    _columns = {
        'name': fields.char('Tên', size=1024, required=True),
    }
    
hang_muc()

class phuongthuc_thanhtoan(osv.osv):
    _name = "phuongthuc.thanhtoan"
    
    _columns = {
        'name': fields.char('Tên', size=1024, required=True),
    }
    
phuongthuc_thanhtoan()

class giai_doan(osv.osv):
    _name = "giai.doan"
    
    _columns = {
        'name': fields.char('Tên', size=1024, required=True),
    }
    
giai_doan()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: