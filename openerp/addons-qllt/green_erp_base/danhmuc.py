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
# class khu_pho(osv.osv):
#     _name = "khu.pho"
#     _columns = {
#         'name': fields.char('Khu phố (ấp)',size = 50, required = True),
#         'quan_huyen_id': fields.many2one( 'quan.huyen','Quận (huyện)', required = True),
#         'phuong_xa_id': fields.many2one( 'phuong.xa','Phường (xã)', required = True),
#                 }
# khu_pho()
class loai_giay_to(osv.osv):
    _name = "loai.giay.to"
    _columns = {
        'name': fields.char('Tên',size = 1024, required = True),
                }
loai_giay_to()
class khach_san(osv.osv):
    _name = "khach.san"
    _columns = {
        'name': fields.char('Tên',size = 1024, required = True),
        'tinh_tp_id': fields.many2one( 'tinh.tp','Tỉnh/TP', required = True),
        'phuong_xa_id': fields.many2one( 'phuong.xa','Phường (xã)', required = True),
        'quan_huyen_id': fields.many2one('quan.huyen','Quận (huyện)', required = True),
        'gpkd': fields.char('Giấy phép KD',size = 1024),
        'tang_ks_line':fields.one2many('tang.ks','ks_id','Tang line'),
        'dien_thoai': fields.char('Điện thoại',size = 1024, required = True),
                }
    
    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
        if context is None:
            context = {}
        if context.get('search_khach_san'):
            sql = '''
                select id from khach_san
                where tinh_tp_id is not null
            '''
            if context.get('tinh_tp_id'):
                sql+='''
                    and tinh_tp_id = %s 
                '''%(context.get('tinh_tp_id'))
            if context.get('quan_huyen_id'):
                sql+='''
                    and quan_huyen_id = %s 
                '''%(context.get('quan_huyen_id'))
            if context.get('phuong_xa_id'):
                sql+='''
                    and phuong_xa_id = %s 
                '''%(context.get('phuong_xa_id'))
            cr.execute(sql)
            ks_ids = [row[0] for row in cr.fetchall()]
            args += [('id','in',ks_ids)]
        return super(khach_san, self).search(cr, uid, args, offset=offset, limit=limit, order=order, context=context, count=count)
    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
       ids = self.search(cr, user, args, context=context, limit=limit)
       return self.name_get(cr, user, ids, context=context)
   
khach_san()
class tang_ks(osv.osv):
    _name = "tang.ks"
    _columns = {
        'name': fields.char('Tầng',size = 1024, required = True),
        'ks_id': fields.many2one('khach.san','Khách sạn'),
        'phong_ks_line':fields.one2many('phong.ks','tang_ks_id','Phòng line'),
                }
tang_ks()

class phong_ks(osv.osv):
    _name = "phong.ks"
    _columns = {
        'name': fields.char('Phòng',size = 1024, required = True),
        'tang_ks_id': fields.many2one('tang.ks','Tầng'),
#         'ks_id_rel':fields.related('tang_ks_line', 'tang_ks_id', type="many2one", relation="khach.san", string="Khach san"),
                }
phong_ks()

class chau_luc(osv.osv):
    _name = "chau.luc"
    _columns = {
        'name': fields.char('Châu lục',size = 1024, required = True),
                }
chau_luc()

class quoc_tich(osv.osv):
    _name = "quoc.tich"
    _columns = {
        'name': fields.char('Quốc tịch',size = 1024, required = True),
        'chau_luc_id': fields.many2one('chau.luc','Châu lục', required = True),
                }
quoc_tich()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
