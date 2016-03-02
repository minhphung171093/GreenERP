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
from datetime import datetime, timedelta
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
            'convert_datetime': self.convert_datetime,
            'convert_date':self.convert_date,
            'get_gioi_tinh': self.get_gioi_tinh,
            'get_quoc_tich': self.get_quoc_tich,
            'get_luu_tru': self.get_luu_tru,
            'get_phong': self.get_phong,
            'get_dia_chi': self.get_dia_chi,
        })

    def convert_date(self, date):
        if date:
            date = datetime.strptime(date, DATE_FORMAT)
            return date.strftime('%d/%m/%Y')
        
    def convert_datetime(self, date):
        if datetime:
            date = datetime.strptime(date, DATETIME_FORMAT) + timedelta(hours=7)
            return date.strftime('%d/%m/%Y %H:%M:%S')
    
    def get_gioi_tinh(self, gioi_tinh):
        if gioi_tinh:
            if gioi_tinh=='name':
                return u'Nam'
            else:
                return u'Nữ'
        else:
            return ''
    
    def get_quoc_tich(self, quoc_tich_id):
        if quoc_tich_id:
            quoc_tich = self.pool.get('quoc.tich').browse(self.cr,self.uid,quoc_tich_id)
            return quoc_tich.name
        else:
            return ''
        
    def get_luu_tru(self, khach_san_id):
        if khach_san_id:
            khach_san = self.pool.get('khach.san').browse(self.cr,self.uid,khach_san_id)
            return khach_san.name
        else:
            return ''
        
    def get_phong(self, phong_ks_id):
        if phong_ks_id:
            phong_ks = self.pool.get('phong.ks').browse(self.cr,self.uid,phong_ks_id)
            return phong_ks.name
        else:
            return ''
    
    def get_dia_chi(self, dia_chi, khach_tinhtp_id, khach_quanhuyen_id, khach_phuongxa_id):
        address = ''
        if dia_chi:
            address += dia_chi + ', '
        if khach_phuongxa_id:
            phuong = self.pool.get('phuong.xa').browse(self.cr,self.uid,khach_phuongxa_id)
            address += phuong.name + ', ' 
        if khach_quanhuyen_id:
            quan = self.pool.get('quan.huyen').browse(self.cr,self.uid,khach_quanhuyen_id)
            address += quan.name + ', ' 
        if khach_tinhtp_id:
            tinh = self.pool.get('tinh.tp').browse(self.cr,self.uid,khach_tinhtp_id)
            address += tinh.name
        return address

    def get_khach_san(self):
        wizard_data = self.localcontext['data']['form']
        quan_huyen_id = wizard_data['quan_huyen_id']
        phuong_xa_id = wizard_data['phuong_xa_id']
        tinh_tp_id = wizard_data['tinh_tp_id']
        khach_san_id = wizard_data['khach_san_id']
        quoc_tich_id = wizard_data['quoc_tich_id']
        tu_ngay = wizard_data['tu_ngay']
        den_ngay = wizard_data['den_ngay']
        sql='''
            select name,gioi_tinh,ngay_sinh,so_giay_to,quoc_tich_id,dia_chi,khach_tinhtp_id,khach_quanhuyen_id,khach_phuongxa_id,
                        khach_san_id,ngay_den,ngay_di,phong_ks_id
            from luu_tru where name is not null 
        '''
        if tinh_tp_id:
            sql+='''
                and tinh_tp_id = %s 
            '''%(tinh_tp_id[0])
        if quan_huyen_id:
            sql+='''
                and quan_huyen_id = %s 
            '''%(quan_huyen_id[0])
        if phuong_xa_id:
            sql+='''
                and phuong_xa_id = %s 
            '''%(phuong_xa_id[0])
        if khach_san_id:
            sql+='''
                and khach_san_id = %s 
            '''%(khach_san_id[0])
        if quoc_tich_id:
            sql+='''
                and quoc_tich_id = %s 
            '''%(quoc_tich_id[0])
        if tu_ngay:
            sql+='''
                and to_char(ngay_den + interval '7 hour', 'YYYY-MM-DD') >= '%s'
            '''%(tu_ngay)
        if den_ngay:
            sql+='''
                and to_char(ngay_den + interval '7 hour', 'YYYY-MM-DD') <= '%s'
            '''%(den_ngay)
        sql+='''
            order by khach_san_id 
        '''
        self.cr.execute(sql)
        return self.cr.dictfetchall()
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

