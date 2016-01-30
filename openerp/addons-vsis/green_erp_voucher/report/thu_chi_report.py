# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp.osv import fields, osv
from openerp import tools
import time
from dateutil.relativedelta import relativedelta
from openerp.tools import config

class report_thu_chi(osv.osv):
    _name = "report.thu.chi"
    _auto = False
    _columns = {
        'name': fields.char('Số', size=1024),
        'user_id': fields.many2one('res.users', 'Nhân viên'),
        'date': fields.date('Tháng'),
        'date_str': fields.char('Ngày'),
        'project_id': fields.many2one('du.an', 'Dự án'),
        'hang_muc_id': fields.many2one('hang.muc', 'Hạng mục'),
        'thu': fields.integer('Thu'),
        'chi': fields.integer('Chi'),
        'con_lai': fields.integer('Số dư'),
        'company_id': fields.many2one('res.company', 'Công ty'),
        'phuongthuc_thanhtoan_id': fields.many2one('phuongthuc.thanhtoan', 'Nguồn tài chính'),
        'type': fields.selection([('thuc_thu','Thực thu'),('thuc_chi','Thực chi'),('du_thu','Dự thu'),('du_chi','Dự chi')], 'Loại'),
        'giai_doan_id': fields.many2one('giai.doan', 'Giai đoạn'),
    }

    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'report_thu_chi')
        sql = '''
            CREATE view report_thu_chi as
                select id, name, user_id, date, project_id, hang_muc_id, company_id, phuongthuc_thanhtoan_id, type, giai_doan_id, date_str,
                    case when type in ('thuc_thu','du_thu') then thanh_tien else 0 end thu,
                    case when type in ('thuc_chi','du_chi') then thanh_tien else 0 end chi,
                    case when type in ('thuc_thu','du_thu') then thanh_tien else -1*thanh_tien end con_lai
                from green_erp_voucher
                
                group by id, name, user_id, date, project_id, hang_muc_id, company_id, phuongthuc_thanhtoan_id, type, giai_doan_id, date_str
        '''
        cr.execute(sql)

report_thu_chi()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: