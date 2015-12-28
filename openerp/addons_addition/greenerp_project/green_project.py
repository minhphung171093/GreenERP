# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, date, timedelta
from lxml import etree
import time

from openerp import api
from openerp import SUPERUSER_ID
from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.exceptions import UserError
from openerp.tools.sql import drop_view_if_exists

class task(osv.osv):
    _inherit = "project.task"
    
    def caculate_day(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for task_id in self.browse(cr, uid, ids, context=context):
            time_total = 0
            sql='''
                select case when sum(hours) != 0 then sum(hours) else 0 end hours from lichsu_task where name=%s and task_id=%s
            '''%(task_id.user_id.id,task_id.id)
            cr.execute(sql)
            hour = cr.fetchone()[0]
            if hour > (task_id.dinh_muc or 0)*8:
                time_total= float(hour-(task_id.dinh_muc or 0)*8)/8.0
            res[task_id.id] = time_total            
        return res
    
    _columns = {
        'loai_cv_id': fields.many2one('loai.cv', 'Loại Công Việc'),
        'dinh_muc': fields.integer('Số Ngày Định Mức'),
        'state': fields.selection([('moi_tao','Mới Tạo'),
                                   ('dang_thuc_hien','Đang Thực Hiện'),
                                   ('tam_ngung', 'Tạm Ngưng'),
                                   ('hoan_thanh','Hoàn Thành')],
                                  'Status'),
        'khoi_tao': fields.boolean('Khoi Tao'),
        'songay_tre': fields.function(caculate_day, string='Số Ngày Trễ hạn', type='float'),
    }
    _defaults = {
        'state': 'moi_tao',
        'date_start': False,
    }
    
    def default_get(self, cr, uid, fields, context=None):
        if context is None:
            context = {}
        res = super(task, self).default_get(cr, uid, fields, context=context)
        res.update({'date_start': False})
        return res
    
    def thuchien(self,cr,uid,ids,context=None):
        vals={}
        res={}
        task_ids = self.search(cr, uid, [('state', '=', 'dang_thuc_hien'),('user_id','=',uid)])
        if task_ids:
            raise UserError(_('Hiện tại bạn đang có một task khác đang được thực hiện.\n Bạn phải hoàn thành hoặc tạm ngưng để có thể thực hiện công việc này!'))
        else:
            if not self.browse(cr,uid,ids[0]).khoi_tao:
                vals.update({'date_start':fields.datetime.now(),
                             'khoi_tao': True,})
            vals.update({'state':'dang_thuc_hien',})
            res = {'name': uid,
                    'task_id': ids[0],
                    'date_start': fields.datetime.now(),
                     }
            self.pool.get('lichsu.task').create(cr,uid,res)
            return self.write(cr, uid, ids,vals)
    
    def tamngung(self,cr,uid,ids,context=None):
        lichsu_obj = self.pool.get('lichsu.task')
        lichsu_ids = lichsu_obj.search(cr, uid, [('name', '=', uid),('task_id','=',ids[0]),('date_end','=',False)])
        if lichsu_ids:
            value = {'date_end': fields.datetime.now,}
            lichsu_obj.write(cr,uid,lichsu_ids,value)
        return self.write(cr, uid, ids,{'state':'tam_ngung'})
    
    def hoanthanh(self,cr,uid,ids,context=None):
#         lichsu_obj = self.pool.get('lichsu.task')
#         lichsu_ids = lichsu_obj.search(cr, uid, [('name', '=', uid),('task_id','=',ids[0]),('date_end','=',False)])
#         if lichsu_ids:
#             value = {'date_end': fields.datetime.now,}
#             lichsu_obj.write(cr,uid,lichsu_ids,value)
        return self.write(cr, uid, ids,{'state':'hoan_thanh'})
    
    def onchange_date_start(self, cr, uid, ids,context=None):
        res = {'value':{
                        'date_start':False,
                      }
               }
        return res
    
    def onchange_loaicv(self, cr, uid, ids,loaicv_id=False,context=None):
        if loaicv_id:
            return {'value':{
                            'dinh_muc':self.pool.get('loai.cv').browse(cr, uid, loaicv_id).dinh_muc or 0,
                          }
                   }
    
task()

class loai_cv(osv.osv):
    _name = "loai.cv"
    _columns = {
        'name': fields.char('Loại Công Việc', size=256, required=True),
        'dinh_muc': fields.integer('Định Mức', required=True),
    }
    
loai_cv()

class lichsu_task(osv.osv):
    _name = "lichsu.task"
    
    def caculate_time(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for lichsu_obj in self.browse(cr, uid, ids, context=context):
            res[lichsu_obj.id] = {
                'hours': 0.0,
            }
            time_total = 0
            if lichsu_obj.date_end:
                time_delta = datetime.strptime(lichsu_obj.date_end,'%Y-%m-%d %H:%M:%S') - datetime.strptime(lichsu_obj.date_start,'%Y-%m-%d %H:%M:%S')
                time_total = time_delta.days*24+float(time_delta.seconds)/float(3600)
            res[lichsu_obj.id]['hours'] = time_total            
        return res
    
    _columns = {
        'name': fields.many2one('res.users', 'User',readonly=True),
        'task_id': fields.many2one('project.task', 'Task',readonly=True),
        'date_start': fields.datetime('Starting Date',readonly=True),
        'date_end': fields.datetime('Ending Date',readonly=True),
        'description':fields.char('Mô Tả', size=256),
        'hours': fields.function(caculate_time, string='Hours', type='float', multi='sums', help="Hours", store=True),
    }
lichsu_task()

class task_cal_report(osv.osv):
    _name = "task.cal.report"
#     _auto = False
    _columns = {
#         'id': fields.integer('Task Id', readonly=True),
        'name': fields.many2one('res.users', 'User'),
        'task_id': fields.many2one('project.task', 'Task'),
        'date_start': fields.date('Starting Date'),
        'date_end': fields.date('Ending Date'),
        'hours': fields.float('Hours'),
    }
#     def init(self, cr):
#         cr.execute('''
#         DROP SEQUENCE IF EXISTS task_cal_report_sequence cascade ;
#         CREATE SEQUENCE task_cal_report_sequence START 1;
#         commit;''')
#         drop_view_if_exists(cr, 'task_cal_report')
#         cr.execute('''CREATE or replace VIEW task_cal_report(id,name,task_id,date_start,date_end,hours)
#             AS (
#             
#             select nextval('task_cal_report_sequence')::integer as id, foo.name as name, foo.task_id as task_id, foo.date_start as date_start,
#                 foo.date_end as date_end, foo.hours as hours
#                 from (
#                     SELECT name,task_id,date(timezone('UTC',date_start)) as date_start,date(timezone('UTC',date_end)) as date_end,sum(hours) as hours
#                         FROM lichsu_task
#                     GROUP BY name,task_id,date(timezone('UTC',date_start)),date(timezone('UTC',date_end))
#                 )foo
#             );
#             commit;''')
task_cal_report()
