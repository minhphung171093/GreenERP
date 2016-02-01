# -*- coding: utf-8 -*-
##############################################################################
#
#    HLVSolution, Open Source Management Solution
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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Parser(report_sxw.rml_parse):
        
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context=context)
        pool = pooler.get_pool(self.cr.dbname)
        self.context = context
        self.localcontext.update({
            'convert_date': self.convert_date,
            'get_lines': self.get_lines,
            'get_loai': self.get_loai,
        })
        
    def convert_date(self, date):
        if date:
            date = datetime.strptime(date, DATE_FORMAT)
            return date.strftime('%d/%m/%Y')
        return ''
    
    def get_lines(self):
        if self.context.get('active_ids', False):
            voucher_ids = self.context['active_ids']
            return self.pool.get('green.erp.voucher').browse(self.cr, self.uid, voucher_ids)
        return []
    
    def get_loai(self, type):
        t=''
        if type=='thuc_thu':
            t='Thực thu'
        if type=='thuc_chi':
            t='Thực chi'
        if type=='du_thu':
            t='Dự thu'
        if type=='du_chi':
            t='Dự chi'
        return t
    