# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp.osv import fields, osv
from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
import time
from openerp import SUPERUSER_ID
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import openerp.addons.decimal_precision as dp
from openerp import netsvc
import datetime
from datetime import date, datetime
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"

from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare

class mo_ta_task(osv.osv_memory):
    _name = "mo.ta.task"
    _columns = {
            'name': fields.char('Lí Do', size=128, required=True),
    }
     
    def bt_luu(self, cr, uid, ids, context=None):
        lichsu_obj = self.pool.get('lichsu.task')
        data = context and context.get('active_ids', []) or []
        value={}
        lichsu_ids = lichsu_obj.search(cr, uid, [('name', '=', uid),('task_id','=',data[0]),('date_end','=',False)])
        if lichsu_ids:
            report_obj = self.pool.get('task.cal.report')
            value = {'date_end': fields.datetime.now(),
                     'description': self.browse(cr,uid,ids[0]).name,}
            lichsu_obj.write(cr,uid,lichsu_ids,value)
            lichsu_id = lichsu_obj.browse(cr,uid,lichsu_ids[0])
            report_ids = report_obj.search(cr, uid, [('name', '=', lichsu_id.name.id),('task_id','=',lichsu_id.task_id.id),('date_start','=',lichsu_id.date_start)])
            if report_ids:
                report_obj.unlink(cr, uid, report_ids, context=context)
            sql=''' SELECT name,task_id,date(timezone('UTC',date_start)) as date_start,date(timezone('UTC',date_end)) as date_end,sum(hours) as hours
                         FROM lichsu_task where name=%s and task_id=%s and date(date_start) = '%s'
                   GROUP BY name,task_id,date(timezone('UTC',date_start)),date(timezone('UTC',date_end)) '''%(lichsu_id.name.id,lichsu_id.task_id.id,lichsu_id.date_start)
            cr.execute(sql)
            res = {}
            for line in cr.dictfetchall():
                res = {
                        'name': line['name'],
                        'task_id': line['task_id'],
                        'date_start': line['date_start'],
                        'date_end': line['date_end'],
                        'hours': line['hours'],
                    }
                report_obj.create(cr,uid,res)
            self.pool.get('project.task').write(cr, uid, data,{'state':'tam_ngung', 'date_end': fields.datetime.now(),})
        return True
    
    def bt_hoanthanh(self, cr, uid, ids, context=None):
        data = context and context.get('active_ids', []) or []
        self.bt_luu(cr, uid, ids, context)
        return self.pool.get('project.task').write(cr, uid, data,{'state':'hoan_thanh'})
        

mo_ta_task()
