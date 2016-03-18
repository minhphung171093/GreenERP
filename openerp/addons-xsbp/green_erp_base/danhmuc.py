# -*- coding: utf-8 -*-
from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from datetime import datetime
import time
from datetime import date
from datetime import timedelta
from datetime import datetime
import calendar
import openerp.addons.decimal_precision as dp
import codecs
import os
# from xlrd import open_workbook,xldate_as_tuple
from openerp import modules

from math import radians, cos, sin, asin, sqrt

class tinh_tp(osv.osv):
    _name = "tinh.tp"
    _columns = {
        'name': fields.char('Tên Tỉnh/Thành Phố',size = 1024, required = True),
        'code': fields.char('Mã Tỉnh/Thành Phố',size = 1024, required = True),
        'stt': fields.integer('STT'),
                }
    
    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if context is None:
            context = {}
        if not name:
            ids = self.search(cr, user, args, limit=limit, context=context)
        else:
            ids = self.search(cr, user, [('code',operator,name)] + args, limit=limit, context=context)
            if not ids:
                ids = self.search(cr, user, [('name',operator,name)] + args, limit=limit, context=context)
            
        return self.name_get(cr, user, ids, context=context)
tinh_tp()
class phuong_xa(osv.osv):
    _name = "phuong.xa"
    _columns = {
        'name': fields.char('Phường (xã)',size = 50, required = True),
        'code': fields.char('Mã Phường/Xã',size = 1024, required = True),
        'quan_huyen_id': fields.many2one( 'quan.huyen','Quận (huyện)', required = True),
                }
    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if context is None:
            context = {}
        if not name:
            ids = self.search(cr, user, args, limit=limit, context=context)
        else:
            ids = self.search(cr, user, [('code',operator,name)] + args, limit=limit, context=context)
            if not ids:
                ids = self.search(cr, user, [('name',operator,name)] + args, limit=limit, context=context)
            
        return self.name_get(cr, user, ids, context=context)
phuong_xa()
class quan_huyen(osv.osv):
    _name = "quan.huyen"
    _columns = {
        'name': fields.char('Quận (huyện)',size = 50, required = True),
        'code': fields.char('Mã Quận/Huyện',size = 1024, required = True),
        'tinh_tp_id':fields.many2one('tinh.tp','Thuộc Tỉnh/Thành phố', required = True),
                }
    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if context is None:
            context = {}
        if not name:
            ids = self.search(cr, user, args, limit=limit, context=context)
        else:
            ids = self.search(cr, user, [('code',operator,name)] + args, limit=limit, context=context)
            if not ids:
                ids = self.search(cr, user, [('name',operator,name)] + args, limit=limit, context=context)
            
        return self.name_get(cr, user, ids, context=context)
quan_huyen()

class res_partner(osv.osv):
    _inherit = "res.partner"
    _columns = {
        'ma_dl': fields.char('Tên đại lý', size=1024),
        'ten': fields.char('Tên đại lý', size=1024, required = True),
        'tinh_tp_id': fields.many2one('tinh.tp','Tỉnh/Thành Phố'),
        'dia_chi': fields.char('Địa chỉ', size=1024),
        'phuong_xa_id': fields.many2one('phuong.xa','Phường (xã)'),
        'quan_huyen_id': fields.many2one('quan.huyen','Quận (huyện)'),
        'ngay': fields.date('Ngày sinh'),
        'ten_gd': fields.char('Tên giao dịch', size=1024),
        'so_dt': fields.char('Số điện thoại', size=1024),
        'kd_tinh_tp_id': fields.many2one('tinh.tp','Tỉnh/Thành Phố'),
        'kd_dia_chi': fields.char('Địa chỉ', size=1024),
        'kd_phuong_xa_id': fields.many2one('phuong.xa','Phường (xã)'),
        'kd_quan_huyen_id': fields.many2one('quan.huyen','Quận (huyện)'),
        'dai_ly': fields.boolean('is_dai_ly'),
        'stt': fields.integer('STT'),
                }
      
    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        res = []
        reads = self.read(cr, uid, ids, ['ten','name'], context)
      
        for record in reads:
            name = record['ten'] + '-' + '['+ record['name'] + ']'
            res.append((record['id'], name))
        return res  
      
    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
        if context is None:
            context = {}
        if context.get('search_dai_ly'):
            if context.get('ky_ve_id') and context.get('loai_ve_id'):
                sql = '''
                    select daily_id from phanphoi_tt_line
                    where phanphoi_tt_id in (select id from phanphoi_truyenthong where ky_ve_id = %s and loai_ve_id = %s)
                '''%(context.get('ky_ve_id'), context.get('loai_ve_id'))
                cr.execute(sql)
                dai_ly_ids = [row[0] for row in cr.fetchall()]
                args += [('id','in',dai_ly_ids)]
            if not context.get('ky_ve_id') or not context.get('loai_ve_id'):
                dai_ly_ids = False
                args += [('id','in',dai_ly_ids)]
        return super(res_partner, self).search(cr, uid, args, offset=offset, limit=limit, order=order, context=context, count=count)
    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
       ids = self.search(cr, user, args, context=context, limit=limit)
       return self.name_get(cr, user, ids, context=context)
     
res_partner()

class cap_ve(osv.osv):
    _name = "cap.ve"
    _columns = {
        'name': fields.float('Cặp vé',digits=(16,0), required = True),
                }
cap_ve()

class khu_vuc(osv.osv):
    _name = "khu.vuc"
    _columns = {
        'name': fields.char('Mã Điểm trả ế',size = 1024, required = True),
        'ten': fields.char('Tên Điểm trả ế',size = 1024, required = True),
                }
khu_vuc()

class ky_ve(osv.osv):
    _name = "ky.ve"
    _columns = {
        'name': fields.char('Mã kỳ vé',size = 1024, required = True),
        'ngay_mo_thuong':fields.date('Ngày mở thưởng', required = True)
                }
    
    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
        if context is None:
            context = {}
        if context.get('search_baocao_kyve'):
            sql = '''
                select id from ky_ve
                where id in (select ky_ve_id from phanphoi_truyenthong)
            '''
            cr.execute(sql)
            ky_ve_ids = [row[0] for row in cr.fetchall()]
            args += [('id','in',ky_ve_ids)]
        if context.get('search_ky_ve'):
            sql = '''
                select id from ky_ve
                where id not in (select ky_ve_id from phanphoi_truyenthong where ky_ve_id is not null)
            '''
            cr.execute(sql)
            ky_ve_ids = [row[0] for row in cr.fetchall()]
            args += [('id','in',ky_ve_ids)]
        if context.get('search_ky_ve_dieuchinh'):
            sql = '''
                select id from ky_ve
                where id in (select ky_ve_id from phanphoi_truyenthong)
            '''
            cr.execute(sql)
            ky_ve_ids = [row[0] for row in cr.fetchall()]
            args += [('id','in',ky_ve_ids)]
        if context.get('search_ky_ve_e'):
            sql = '''
                select id from ky_ve
                where id not in (select ky_ve_id from nhap_ve_e where ky_ve_id is not null) and id in (select ky_ve_id from phanphoi_truyenthong)
            '''
            cr.execute(sql)
            ky_ve_ids = [row[0] for row in cr.fetchall()]
            args += [('id','in',ky_ve_ids)]
        return super(ky_ve, self).search(cr, uid, args, offset=offset, limit=limit, order=order, context=context, count=count)
    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
       ids = self.search(cr, user, args, context=context, limit=limit)
       return self.name_get(cr, user, ids, context=context)
ky_ve()

class loai_ve(osv.osv):
    _name = "loai.ve"
    _columns = {
        'name': fields.char('Loại vé',size = 1024, required = True),
        'gia_tri': fields.float('Gía trị', required = True),
                }
loai_ve()

class loai_hinh(osv.osv):
    _name = "loai.hinh"
    _columns = {
        'name': fields.char('Tên',size = 1024, required = True),
        'doanh_thu': fields.selection([('xs','Xổ số'), ('ks','Khách sạn')], 'Doanh thu', required = True),
        'parent_id': fields.many2one('loai.hinh','Parent Loai Hinh'),
#         'loai_hinh_line': fields.one2many('loai.hinh.line','loai_hinh_id','Loai hinh line'),
                }
#     def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
#         if context is None:
#             context = {}
#         if context.get('search_dai_ly'):
#             if context.get('ky_ve_id') and context.get('loai_ve_id'):
#                 sql = '''
#                     select daily_id from phanphoi_tt_line
#                     where phanphoi_tt_id in (select id from phanphoi_truyenthong where ky_ve_id = %s and loai_ve_id = %s)
#                 '''%(context.get('ky_ve_id'), context.get('loai_ve_id'))
#                 cr.execute(sql)
#                 dai_ly_ids = [row[0] for row in cr.fetchall()]
#                 args += [('id','in',dai_ly_ids)]
#         return super(dai_ly, self).search(cr, uid, args, offset=offset, limit=limit, order=order, context=context, count=count)
#     def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
#        ids = self.search(cr, user, args, context=context, limit=limit)
#        return self.name_get(cr, user, ids, context=context)
loai_hinh()
class loai_hinh_line(osv.osv):
    _name = "loai.hinh.line"
    _columns = {
        'name': fields.char('Tên',size = 1024, required = True),
        'is_ty_le': fields.boolean('Có tính tỉ lệ'),
        'loai_hinh_id': fields.many2one('loai.hinh','Loại hình',ondelete="cascade"),
                }
loai_hinh_line()

class ds_dai(osv.osv):
    _name = "ds.dai"
    _columns = {
        'name': fields.char('Tên',size = 1024, required = True),
                }
ds_dai()

class nhap_doanhthu(osv.osv):
    _name = "nhap.doanhthu"
    _columns = {
        'name': fields.date('Ngày', required = True),
        'dai_id': fields.many2one('ds.dai','Đài', required = True),
        'doanh_thu': fields.float('Doanh Thu', required = True),
                }
nhap_doanhthu()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
