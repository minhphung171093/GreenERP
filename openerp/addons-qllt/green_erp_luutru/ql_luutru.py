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

class luu_tru(osv.osv):
    _name = "luu.tru"
    _columns = {
        'name': fields.char('Họ và Tên',size = 1024, required = True),
        'ngay_sinh':fields.date('Ngày tháng năm sinh',required = True),
        'khach_san_id': fields.many2one( 'khach.san','Nơi lưu trú', required = True),
        'tinh_tp_id': fields.many2one( 'tinh.tp','Tỉnh/TP', readonly = True),
        'phuong_xa_id': fields.many2one( 'phuong.xa','Phường (xã)', readonly = True),
        'quan_huyen_id': fields.many2one('quan.huyen','Quận (huyện)', readonly = True),
        'khach_tinhtp_id': fields.many2one( 'tinh.tp','Tỉnh/TP', required = True),
        'khach_phuongxa_id': fields.many2one( 'phuong.xa','Phường (xã)', required = True),
        'khach_quanhuyen_id': fields.many2one('quan.huyen','Quận (huyện)', required = True),
        'gioi_tinh':fields.selection([('nam', 'Nam'),
                                  ('nu', 'Nữ'),
                                  ],'Giới tính'),
        'loai_giay_to_id': fields.many2one('loai.giay.to','Loại giấy tờ', required = True),
        'so_giay_to': fields.char('Số giấy tờ',required = True,size = 1024),
        'quoc_tich': fields.char('Quốc tịch',required = True,size = 1024),
        'ngay_den':fields.datetime('Ngày giờ đến',required = True),
        'ngay_di':fields.datetime('Ngày giờ đi',required = True),
        'tang_ks_id': fields.many2one('tang.ks','Tầng', required = True),
        'phong_ks_id': fields.many2one('phong.ks','Phòng', required = True),
        'dien_thoai': fields.char('Điện thoại',size = 1024, readonly = True),
        'tiep_nhan': fields.char('Họ tên CA tiếp nhận',size = 1024, required = True),
        'ghi_chu': fields.char('Ghi chú',size = 1024),
                }
    _defaults = {
        'ngay_den':  lambda *a: time.strftime('%Y-%m-%d'),        
                 }
    def on_change_diachi(self, cr, uid, ids, khach_san_id=False):
        res = {'value':{
                        'tinh_tp_id':False,
                        'phuong_xa_id':False,
                        'quan_huyen_id':False,
                        'dien_thoai': False,
                      }
               }
        if khach_san_id:
            ks = self.pool.get('khach.san').browse(cr, uid, khach_san_id)
            res['value'].update({
                                'tinh_tp_id':ks.tinh_tp_id.id,
                                'phuong_xa_id':ks.phuong_xa_id.id,
                                'quan_huyen_id':ks.quan_huyen_id.id,
                                'dien_thoai': ks.dien_thoai,
                                })
            
        return res
luu_tru()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
