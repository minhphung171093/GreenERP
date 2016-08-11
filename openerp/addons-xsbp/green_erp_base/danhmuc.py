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
        'tinh_tp_id': fields.many2one('tinh.tp','Tỉnh/Thành Phố', required = True),
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
        'tinh_tp_id': fields.many2one('tinh.tp','Tỉnh/Thành Phố', required = True),
                }
ds_dai()

class zz_dim_kyve0(osv.osv):
    _name = "zz.dim.kyve0"
    _auto = False
    _columns = {
        'kyve_key': fields.many2one('ky.ve','KyVe_key'),
        'tenkyve': fields.char('TenKyVe',size = 1024),
    }
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'zz_dim_kyve0')
        cr.execute("""
            create or replace view zz_dim_kyve0 as (
                select id as kyve_key, name as tenkyve
                    from ky_ve
            )
        """)
zz_dim_kyve0()

class zz_dim_daily0(osv.osv):
    _name = "zz.dim.daily0"
    _auto = False
    _columns = {
        'daily_key': fields.many2one('res.partner','DaiLy_Key'),
        'tendaily': fields.char('TenDaiLy',size = 1024),
        'tentinh': fields.char('TenTinh',size = 1024),
        'tenquanhuyen': fields.char('TenQuanHuyen',size = 1024),
        'tenphuongxa': fields.char('TenPhuongXa',size = 1024),
    }
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'zz_dim_daily0')
        cr.execute("""
            create or replace view zz_dim_daily0 as (
                select rp.id as daily_key, rp.name as tendaily, t.name as tentinh,
                    qh.name as tenquanhuyen, px.name as tenphuongxa
                    from res_partner rp
                    left join tinh_tp t on rp.tinh_tp_id=t.id
                    left join quan_huyen qh on rp.quan_huyen_id=qh.id
                    left join phuong_xa px on rp.phuong_xa_id=px.id
                where dai_ly=True
            )
        """)
zz_dim_kyve0()

class zz_fact_doanhthuphathanhsx0(osv.osv):
    _name = "zz.fact.doanhthuphathanhsx0"
    _auto = False
    _columns = {
        'doanhthu': fields.float('Doanh thu', digits=(16,0)),
        'phathanh': fields.float('Phat hanh', digits=(16,0)),
        'ngay_key': fields.date('Ngày mở thưởng'),
        'daily_key': fields.many2one('res.partner','Đại lý'),
        'kyve_key': fields.many2one('ky.ve','Kỳ vé'),
    }
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'zz_fact_doanhthuphathanhsx0')
        cr.execute("""
            create or replace view zz_fact_doanhthuphathanhsx0 as (

                select daily_id as daily_key, ky_ve_id as kyve_key, sum(doanhthu) as doanhthu, sum(phathanh) as phathanh, ngay_mo_thuong as ngay_key
                from
                (
                select ppttl.daily_id as daily_id, pptt.ky_ve_id as ky_ve_id,
                    case when (select sove_sau_dc from dieuchinh_line where phanphoi_line_id=ppttl.id order by id desc limit 1) is not null
                        then (select sove_sau_dc*lv.gia_tri from dieuchinh_line where phanphoi_line_id=ppttl.id order by id desc limit 1) else ppttl.sove_kynay*lv.gia_tri end doanhthu,
                    
                    0 as phathanh,
                    kv.ngay_mo_thuong as ngay_mo_thuong
                    from phanphoi_tt_line ppttl 
                    left join phanphoi_truyenthong pptt on ppttl.phanphoi_tt_id=pptt.id
                    left join loai_ve lv on pptt.loai_ve_id = lv.id
                    left join ky_ve kv on pptt.ky_ve_id = kv.id
                union all
                
                select vel.daily_id as daily_id, ve.ky_ve_id as ky_ve_id,-1*vel.thuc_kiem*lv.gia_tri as doanhthu,0 as phathanh, 
                kv.ngay_mo_thuong as ngay_mo_thuong
                
                    from nhap_ve_e_line vel
                    left join nhap_ve_e ve on vel.nhap_ve_e_id=ve.id
                    left join loai_ve lv on ve.loai_ve_id = lv.id
                    left join ky_ve kv on ve.ky_ve_id = kv.id
                union all

                select ppttl.daily_id as daily_id, pptt.ky_ve_id as ky_ve_id,
                    0 as doanhthu,
                    case when (select sove_sau_dc from dieuchinh_line where phanphoi_line_id=ppttl.id order by id desc limit 1) is not null
                        then (select sove_sau_dc*lv.gia_tri from dieuchinh_line where phanphoi_line_id=ppttl.id order by id desc limit 1) else ppttl.sove_kynay*lv.gia_tri end phathanh,
                    kv.ngay_mo_thuong as ngay_mo_thuong
                    from phanphoi_tt_line ppttl 
                    left join phanphoi_truyenthong pptt on ppttl.phanphoi_tt_id=pptt.id
                    left join loai_ve lv on pptt.loai_ve_id = lv.id
                    left join ky_ve kv on pptt.ky_ve_id = kv.id
                )foo
                group by daily_id,ky_ve_id,ngay_mo_thuong
            )
        """)
zz_fact_doanhthuphathanhsx0()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
