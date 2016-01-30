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
        'thanh_tien': fields.float('Thành tiền', digits=(16,0)),
        'company_id': fields.many2one('res.company', 'Công ty'),
        'phuongthuc_thanhtoan_id': fields.many2one('phuongthuc.thanhtoan', 'Nguồn tài chính'),
        'type': fields.selection([('thuc_thu','Thực thu'),('thuc_chi','Thực chi'),('du_thu','Dự thu'),('du_chi','Dự chi')], 'Loại'),
        'ghi_chu': fields.text('Ghi chú'),
        'giai_doan_id': fields.many2one('giai.doan', 'Giai đoạn'),
        'tamung_id': fields.many2one('green.erp.tamung', 'Tạm ứng'),
    }
    
    def _get_company(self, cr, uid, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid)
        return user.company_id and user.company_id.id or False
    
    def _get_phuongthuc_thanhtoan(self, cr, uid, context=None):
        pttt_ids = self.pool.get('phuongthuc.thanhtoan').search(cr, uid, [('code','=','TM')])
        return pttt_ids and pttt_ids[0] or False
    
    _defaults = {
        'user_id': lambda self, cr, uid, context=None: uid,
        'company_id': _get_company,
        'date': time.strftime('%Y-%m-%d'),
        'name': '/',
        'thanh_tien': 0,
        'phuongthuc_thanhtoan_id': _get_phuongthuc_thanhtoan,
    }
    
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if vals.get('name', '/') == '/' or 'name' not in vals:
            vals['name'] = self.pool.get('ir.sequence').get(cr, 1, 'greenerp_thuchi', context=context) or '/'
        return super(green_erp_voucher, self).create(cr, uid, vals, context)
    
    def bt_taothucchi(self, cr, uid, ids, context=None):
        if context.get('active_id', False):
            self.pool.get('green.erp.tamung').write(cr, uid, [context['active_id']],{'state':'da_chi','thuc_chi_id':ids[0]})
        return True
    
green_erp_voucher()

class green_erp_tamung(osv.osv):
    _name = "green.erp.tamung"
    _order = 'date desc'
    
    def _get_tongthuctechi(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for tamung in self.browse(cr, uid, ids, context=context):
            res[tamung.id] = 0
            tong = 0
            for line in tamung.thucte_chi_line:
                tong += line.thanh_tien
            res[tamung.id] = tong
            if tong and tong<tamung.thanh_tien:
                self.write(cr, uid, [tamung.id], {'state':'cho_thu'})
            if tong and tong>tamung.thanh_tien:
                self.write(cr, uid, [tamung.id], {'state':'cho_tra'})
            if tong and tong==tamung.thanh_tien:
                self.write(cr, uid, [tamung.id], {'state':'hoan_thanh'})
        return res
    
    def _get_tamung(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('green.erp.voucher').browse(cr, uid, ids, context=context):
            result[line.tamung_id.id] = True
        return result.keys()
    
    _columns = {
        'name': fields.char('Số', size=1024),
        'user_id': fields.many2one('res.users', 'Nhân viên', readonly=True, states={'moi_tao': [('readonly', False)]}),
        'date': fields.date('Ngày', readonly=True, states={'moi_tao': [('readonly', False)]}),
        'project_id': fields.many2one('du.an', 'Dự án', readonly=True, states={'moi_tao': [('readonly', False)]}),
        'noi_dung': fields.text('Nội dung', readonly=True, states={'moi_tao': [('readonly', False)]}),
        'hang_muc_id': fields.many2one('hang.muc', 'Hạng mục', readonly=True, states={'moi_tao': [('readonly', False)]}),
        'thanh_tien': fields.float('Số tiền tạm ứng', digits=(16,0), readonly=True, states={'moi_tao': [('readonly', False)]}),
        'company_id': fields.many2one('res.company', 'Công ty', readonly=True, states={'moi_tao': [('readonly', False)]}),
        'phuongthuc_thanhtoan_id': fields.many2one('phuongthuc.thanhtoan', 'Nguồn tài chính', readonly=True, states={'moi_tao': [('readonly', False)]}),
        'ghi_chu': fields.text('Ghi chú'),
        'sotien_thucchi': fields.function(_get_tongthuctechi, string='Tổng thực tế chi', digits=(16,0), type='float', store={
                'green.erp.tamung': (lambda self, cr, uid, ids, c={}: ids, ['thucte_chi_line'], 10),
                'so.tien.lai': (_get_tamung, ['tamung_id', 'thanh_tien'], 10),
            }),
        'state': fields.selection([('moi_tao','Mới tạo'),('da_chi','Chờ quyết toán'),('cho_tra','Chờ chi'),('cho_thu','Chờ thu'),('hoan_thanh','Hoàn thành')], 'Trạng thái'),
        'thuc_chi_id': fields.many2one('green.erp.voucher', 'Thực chi'),
        'thucte_chi_line': fields.one2many('green.erp.voucher', 'tamung_id', 'Thực tế chi', readonly=True, states={'da_chi': [('readonly', False)]}),
    }
    
    def _get_company(self, cr, uid, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid)
        return user.company_id and user.company_id.id or False
    
    def _get_phuongthuc_thanhtoan(self, cr, uid, context=None):
        pttt_ids = self.pool.get('phuongthuc.thanhtoan').search(cr, uid, [('code','=','TM')])
        return pttt_ids and pttt_ids[0] or False
    
    _defaults = {
        'user_id': lambda self, cr, uid, context=None: uid,
        'company_id': _get_company,
        'date': time.strftime('%Y-%m-%d'),
        'name': '/',
        'thanh_tien': 0,
        'phuongthuc_thanhtoan_id': _get_phuongthuc_thanhtoan,
        'state': 'moi_tao',
    }
    
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if vals.get('name', '/') == '/' or 'name' not in vals:
            vals['name'] = self.pool.get('ir.sequence').get(cr, 1, 'greenerp_tamung', context=context) or '/'
        return super(green_erp_tamung, self).create(cr, uid, vals, context)
    
    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('thucte_chi_line', False):
            for line in self.browse(cr, uid, ids):
                if line.thuc_chi_id:
                    sql = '''
                        delete from green_erp_voucher where id=%s
                    '''%(line.thuc_chi_id.id)
                    cr.execute(sql)
        return super(green_erp_tamung, self).write(cr, uid, ids, vals, context)
    
green_erp_tamung()

class du_an(osv.osv):
    _name = "du.an"
    
    _columns = {
        'name': fields.char('Tên', size=1024, required=True),
        'company_id': fields.many2one('res.company', 'Công ty', required=True),
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
        'code': fields.char('Mã', size=1024, required=True),
    }
    
phuongthuc_thanhtoan()

class giai_doan(osv.osv):
    _name = "giai.doan"
    
    _columns = {
        'name': fields.char('Tên', size=1024, required=True),
    }
    
giai_doan()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: