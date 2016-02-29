# -*- coding: utf-8 -*-
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
import time
from openerp.report import report_sxw
from openerp import pooler
from openerp.osv import osv
from openerp.tools.translate import _
import random
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"

from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class Parser(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context=context)
        pool = pooler.get_pool(self.cr.dbname)
        self.localcontext.update({
            'get_khach_san': self.get_khach_san,
#             'get_cell': self.get_cell,
#             'get_col': self.get_col,
#             'get_ho_row': self.get_ho_row,
#             'get_loaivat': self.get_loaivat,
#             'convert_date':self.convert_date,
#             'get_tongcong': self.get_tongcong,
        })

#     def convert_date(self, ten_ho_id):
#         sql = '''
#             select ngay_ghi_so from co_cau where ten_ho_id = %s and trang_thai_id in (select id from trang_thai where stt = 3)
#             group by ngay_ghi_so
#             order by ngay_ghi_so desc
#         '''%(ten_ho_id)
#         self.cr.execute(sql)
#         date = self.cr.dictfetchone()['ngay_ghi_so']
#         if date:
#             date = datetime.strptime(date, DATE_FORMAT)
#         return date.strftime('%d/%m/%Y')
#         
#     def get_tenho(self,ten_ho_id):
#         ten = self.pool.get('chan.nuoi').browse(self.cr,self.uid,ten_ho_id)
#         return ten.name
    

    def get_khach_san(self):
        wizard_data = self.localcontext['data']['form']
        quan_huyen_id = wizard_data['quan_huyen_id']
        phuong_xa_id = wizard_data['phuong_xa_id']
        tinh_tp_id = wizard_data['tinh_tp_id']
        khach_san_id = wizard_data['khach_san_id']
        ngay_den = wizard_data['tu_ngay']
        ngay_di = wizard_data['den_ngay']
        sql='''
            select name,ngay_sinh,khach_san_id,khach_tinhtp_id,khach_phuongxa_id,
                        khach_quanhuyen_id,gioi_tinh,so_giay_to,quoc_tich
            from luu_tru
        '''
        if tinh_tp_id:
            sql+='''
                and tinh_tp_id = %s
            '''%(tinh_tp_id[0])
        if tinh_tp_id and quan_huyen_id:
            sql+='''
                and tinh_tp_id = %s and quan_huyen_id = %s
            '''%(tinh_tp_id[0],quan_huyen_id[0])
        if tinh_tp_id and quan_huyen_id and phuong_xa_id:
            sql+='''
                and tinh_tp_id = %s and quan_huyen_id = %s and phuong_xa_id = %s 
            '''%(tinh_tp_id[0],quan_huyen_id[0],phuong_xa_id[0])
        if tinh_tp_id and quan_huyen_id and phuong_xa_id and khach_san_id:
            sql+='''
                and tinh_tp_id = %s and quan_huyen_id = %s and phuong_xa_id = %s and khach_san_id = %s
            '''%(tinh_tp_id[0],quan_huyen_id[0],phuong_xa_id[0], khach_san_id[0])
        sql+='''
             group by khach_san_id
            order by khach_san_id 
        '''
        self.cr.execute(sql)
        return self.cr.dictfetchall()
    
#     def get_tongcong(self, row):
#         wizard_data = self.localcontext['data']['form']
#         ten_ho_id = wizard_data['ten_ho_id']
#         soluong = 0
#         if row:
#             sql = '''
#                 select case when sum(tong_sl)!=0 then sum(tong_sl) else 0 end tong_sl from chi_tiet_loai_line where
#                     co_cau_id in (select id from co_cau where ten_ho_id = %s and trang_thai = 'new'
#                     and trang_thai_id in (select id from trang_thai where stt = 3))
#             '''%(row)
#             self.cr.execute(sql)
#             test = self.cr.dictfetchone()
#             soluong = test and test['tong_sl'] or False
#         return soluong
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

