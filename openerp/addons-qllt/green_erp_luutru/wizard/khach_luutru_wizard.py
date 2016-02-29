# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.tools
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare


class khach_luutru_form(osv.osv_memory):
    _name = "khach.luutru.form"
    _columns = {    
                'khach_san_id': fields.many2one( 'khach.san','Khách sạn'),
                'phuong_xa_id': fields.many2one( 'phuong.xa','Phường (xã)'),
                'tinh_tp_id': fields.many2one( 'tinh.tp','Tỉnh/TP'),
                'quan_huyen_id': fields.many2one( 'quan.huyen','Quận (huyện)' ),
                'tu_ngay':fields.date('Từ ngày'),
                'tu_ngay':fields.date('Đến ngày'),
                }
    def onchange_quan_huyen(self, cr, uid, ids, context=None):
        vals = {}
        vals = {'phuong_xa_id':False}
        return {'value': vals}
    def onchange_phuong_xa(self, cr, uid, ids, context=None):
        vals = {}
        vals = {'khach_san_id':False}
        return {'value': vals}
    def onchange_tinh_thanh(self, cr, uid, ids, context=None):
        vals = {}
        vals = {'quan_huyen_id':False}
        return {'value': vals}
    def print_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'khach.luutru.form'
        datas['form'] = self.read(cr, uid, ids)[0]
        datas['form'].update({'active_id':context.get('active_ids',False)})
        return {'type': 'ir.actions.report.xml', 'report_name': 'khach_luutru_report', 'datas': datas}
        
khach_luutru_form()