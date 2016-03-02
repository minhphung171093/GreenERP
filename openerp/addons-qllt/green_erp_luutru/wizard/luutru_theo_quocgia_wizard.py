# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.tools
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare


class luutru_quocgia_form(osv.osv_memory):
    _name = "luutru.quocgia.form"
    _columns = {    
                'tu_ngay':fields.date('Từ ngày', required = True),
                'den_ngay':fields.date('Đến ngày', required = True),
                }
    def print_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'luutru.quocgia.form'
        datas['form'] = self.read(cr, uid, ids)[0]
        datas['form'].update({'active_id':context.get('active_ids',False)})
        return {'type': 'ir.actions.report.xml', 'report_name': 'luutru_quocgia_report', 'datas': datas}
        
luutru_quocgia_form()