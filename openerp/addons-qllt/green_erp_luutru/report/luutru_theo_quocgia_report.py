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
            'get_lines': self.get_lines,
            'convert_datetime': self.convert_datetime,
            'convert_date':self.convert_date,
            'get_ngay': self.get_ngay,
        })

    def convert_date(self, date):
        if date:
            date = datetime.strptime(date, DATE_FORMAT)
            return date.strftime('%d/%m/%Y')
        
    def convert_datetime(self, date):
        if datetime:
            date = datetime.strptime(date, DATETIME_FORMAT) + timedelta(hours=7)
            return date.strftime('%d/%m/%Y %H:%M:%S')
    
    def get_ngay(self):
        wizard_data = self.localcontext['data']['form']
        tu_ngay = wizard_data['tu_ngay']
        den_ngay = wizard_data['den_ngay']
        return self.convert_date(tu_ngay)+' - '+self.convert_date(den_ngay)
    

    def get_lines(self):
        wizard_data = self.localcontext['data']['form']
        tu_ngay = wizard_data['tu_ngay']
        den_ngay = wizard_data['den_ngay']
        mang = []
        sql='''
            select id, name from chau_luc
        '''
        self.cr.execute(sql)
        for chau_luc in self.cr.dictfetchall():
            total_tong_cong = 0
            total_theongay = 0
            line_ids = []
            sql='''
                select quoc_tich_id, count(id) as total from luu_tru where quoc_tich_id in (select id from quoc_tich where chau_luc_id = %s)
                group by quoc_tich_id
            '''%(chau_luc['id'])
            self.cr.execute(sql)
            for tong_cong in self.cr.dictfetchall():
                quoc_tich = self.pool.get('quoc.tich').browse(self.cr,self.uid,tong_cong['quoc_tich_id'])
                sql='''
                    select quoc_tich_id, count(id) as theo_ngay from luu_tru where quoc_tich_id = %s 
                    and to_char(ngay_den + interval '7 hour', 'YYYY-MM-DD') between '%s' and '%s'
                    group by quoc_tich_id
                '''%(tong_cong['quoc_tich_id'], tu_ngay, den_ngay)
                self.cr.execute(sql)
                for theo_ngay in self.cr.dictfetchall(): 
                    line_ids.append({
                                     'seq': '1',
                                     'ten': quoc_tich.name,
                                     'total': tong_cong['total'],
                                     'theo_ngay': theo_ngay['theo_ngay'],
                                     })
                    total_tong_cong += tong_cong['total']
                    total_theongay += theo_ngay['theo_ngay']
            mang.append({
                         'seq': '',
                         'ten': chau_luc['name'],
                         'total': total_tong_cong,
                         'theo_ngay': total_theongay,
                         })
            for line in line_ids:
                mang.append({
                         'ten': line['ten'],
                         'total': line['total'],
                         'theo_ngay': line['theo_ngay'],
                         'seq': line['seq']
                         })
            return mang
            
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

