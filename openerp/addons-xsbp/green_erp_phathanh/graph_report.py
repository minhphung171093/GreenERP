# -*- coding: utf-8 -*-
from openerp import tools
from openerp.osv import osv, fields

class doanhthu_graph_report(osv.osv):
    _name = "doanhthu.graph.report"
    _description = "Báo cáo doanh thu"
    _auto = False
    _columns = {
        'daily_id': fields.many2one('res.partner','Đại lý'),
        'ky_ve_id': fields.many2one('ky.ve','Kỳ vé'),
        'giatri': fields.float('Doanh thu', digits=(16,0)),
        'ngay_mo_thuong': fields.date('Ngày mở thưởng'),
        'diem_tra_e_id': fields.many2one('khu.vuc','Thị Trường'),
    }
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'doanhthu_graph_report')
        cr.execute("""
            create or replace view doanhthu_graph_report as (
 
                select id, daily_id, ky_ve_id, sum(giatri) as giatri, ngay_mo_thuong, diem_tra_e_id as thi_truong
                from
                (
                select ppttl.id as id, ppttl.daily_id as daily_id, pptt.ky_ve_id as ky_ve_id,
                    case when (select sove_sau_dc from dieuchinh_line where phanphoi_line_id=ppttl.id order by id desc limit 1) is not null
                        then (select sove_sau_dc*lv.gia_tri from dieuchinh_line where phanphoi_line_id=ppttl.id order by id desc limit 1) else ppttl.sove_kynay*lv.gia_tri end giatri,
                    kv.ngay_mo_thuong as ngay_mo_thuong, vel.diem_tra_e_id as diem_tra_e_id
                    
                    from phanphoi_tt_line ppttl 
                    left join phanphoi_truyenthong pptt on ppttl.phanphoi_tt_id=pptt.id
                    left join loai_ve lv on pptt.loai_ve_id = lv.id
                    left join ky_ve kv on pptt.ky_ve_id = kv.id
                    left join nhap_ve_e_line vel on vel.phanphoi_line_id = ppttl.id
                     
                union all
                 
                select vel.phanphoi_line_id as id, vel.daily_id as daily_id, ve.ky_ve_id as ky_ve_id,-1*vel.thuc_kiem*lv.gia_tri as giatri, kv.ngay_mo_thuong as ngay_mo_thuong,
                    vel.diem_tra_e_id as diem_tra_e_id
                    
                    from nhap_ve_e_line vel
                    left join nhap_ve_e ve on vel.nhap_ve_e_id=ve.id
                    left join loai_ve lv on ve.loai_ve_id = lv.id
                    left join ky_ve kv on ve.ky_ve_id = kv.id
                )foo
                group by id,daily_id,ky_ve_id,ngay_mo_thuong,diem_tra_e_id
            )
        """)
doanhthu_graph_report()
class dthu_phanh_graph_report(osv.osv):
    _name = "dthu.phanh.graph.report"
    _description = "Báo cáo doanh thu và phát hành cho đại lý"
    _auto = False
    _columns = {
        'daily_id': fields.many2one('res.partner','Đại lý'),
        'ky_ve_id': fields.many2one('ky.ve','Kỳ vé'),
        'giatri': fields.float('Giá Trị', digits=(16,0)),
        'loai_giatri': fields.char('Loại'),
        'ngay_mo_thuong': fields.date('Ngày mở thưởng'),
    }
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'dthu_phanh_graph_report')
        cr.execute("""
            create or replace view dthu_phanh_graph_report as (

                select id, daily_id, ky_ve_id, sum(giatri) as giatri, loai_giatri, ngay_mo_thuong
                from
                (
                select ppttl.id as id, ppttl.daily_id as daily_id, pptt.ky_ve_id as ky_ve_id,
                    case when (select sove_sau_dc from dieuchinh_line where phanphoi_line_id=ppttl.id order by id desc limit 1) is not null
                        then (select sove_sau_dc*lv.gia_tri from dieuchinh_line where phanphoi_line_id=ppttl.id order by id desc limit 1) else ppttl.sove_kynay*lv.gia_tri end giatri,
                    
                    'Doanh Thu' as loai_giatri,
                    kv.ngay_mo_thuong as ngay_mo_thuong
                    from phanphoi_tt_line ppttl 
                    left join phanphoi_truyenthong pptt on ppttl.phanphoi_tt_id=pptt.id
                    left join loai_ve lv on pptt.loai_ve_id = lv.id
                    left join ky_ve kv on pptt.ky_ve_id = kv.id
                union all
                
                select vel.phanphoi_line_id as id, vel.daily_id as daily_id, ve.ky_ve_id as ky_ve_id,-1*vel.thuc_kiem*lv.gia_tri as giatri,'Doanh Thu' as loai_giatri, 
                kv.ngay_mo_thuong as ngay_mo_thuong
                
                    from nhap_ve_e_line vel
                    left join nhap_ve_e ve on vel.nhap_ve_e_id=ve.id
                    left join loai_ve lv on ve.loai_ve_id = lv.id
                    left join ky_ve kv on ve.ky_ve_id = kv.id
                union all

                select ppttl.id as id, ppttl.daily_id as daily_id, pptt.ky_ve_id as ky_ve_id, 
                    case when (select sove_sau_dc from dieuchinh_line where phanphoi_line_id=ppttl.id order by id desc limit 1) is not null
                        then (select sove_sau_dc*lv.gia_tri from dieuchinh_line where phanphoi_line_id=ppttl.id order by id desc limit 1) else ppttl.sove_kynay*lv.gia_tri end giatri,
                    
                    'Phát Hành' as loai_giatri,
                    kv.ngay_mo_thuong as ngay_mo_thuong
                    from phanphoi_tt_line ppttl 
                    left join phanphoi_truyenthong pptt on ppttl.phanphoi_tt_id=pptt.id
                    left join loai_ve lv on pptt.loai_ve_id = lv.id
                    left join ky_ve kv on pptt.ky_ve_id = kv.id
                )foo
                group by id,daily_id,ky_ve_id,loai_giatri,ngay_mo_thuong
            )
        """)
dthu_phanh_graph_report()

class loaihinh_graph_report(osv.osv):
    _name = "loaihinh.graph.report"
    _description = "Báo cáo theo loại hình"
    _auto = False
    _columns = {
        'year': fields.selection([(num, str(num)) for num in range(2013, 2050)], 'Năm'),
        'thang': fields.integer('Tháng'),
        'loai_hinh_id': fields.many2one('loai.hinh','Loại hình'),
        'parent_id': fields.many2one('loai.hinh','Parent Loai Hinh'),
        'thuc_hien': fields.float('Thực hiện',digits=(16,0)),
    }
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'loaihinh_graph_report')
        cr.execute("""
            create or replace view loaihinh_graph_report as (
 
                select dtttl.id, dttlh.year, dtttl.thang, dttlh.loai_hinh_id, lh.parent_id, dtttl.thuc_hien
                    
                from dt_theo_thang_line dtttl 
                left join doanhthu_theo_loaihinh dttlh on dtttl.doanh_thu_id=dttlh.id
                left join loai_hinh lh on dttlh.loai_hinh_id = lh.id
                     
            )
        """)
loaihinh_graph_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
