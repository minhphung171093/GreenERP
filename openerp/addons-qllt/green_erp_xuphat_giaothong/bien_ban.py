# -*- coding: utf-8 -*-

import time

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from datetime import datetime
import openerp.addons.decimal_precision as dp

class can_bo(osv.osv):
    _name = "can.bo"
    _columns = {
        'name': fields.char('Tên cán bộ', size=30,required = True),
        'cap_bac': fields.char( 'Cấp bậc',size = 50),
        'chuc_vu': fields.char( 'Chức vụ',size = 50),
        'don_vi_id': fields.many2one( 'don.vi','Đơn vị'),
                }
can_bo()
class don_vi(osv.osv):
    _name = "don.vi"
    _columns = {
        'name': fields.char('Đơn vị', size=30,required = True),
                }
don_vi()
class tam_giu(osv.osv):
    _name = "tam.giu"
    _columns = {
        'name': fields.char('Tạm giữ', size=30,required = True),
                }
tam_giu()
class vi_pham(osv.osv):
    _name = "vi.pham"
    _columns = {
        'name': fields.char('Mã lỗi', size=30,required = True),
        'noi_dung': fields.char( 'Nội dung',size = 50),
        'nghi_dinh': fields.many2one( 'nghi.dinh','Nghị định'),
        'vi_pham_id': fields.many2one('bien.ban'),
                }
vi_pham()
class nghi_dinh(osv.osv):
    _name = "nghi.dinh"
    _columns = {
        'name': fields.char('Mã nghị định', size=30,required = True),
        'noi_dung': fields.char( 'Nội dung',size = 50),
                }
nghi_dinh()
class phuong_tien(osv.osv):
    _name = "phuong.tien"
    _columns = {
        'name': fields.char('Biển số', size=30,required = True),
        'nhan_hieu': fields.char( 'Nhãn hiệu',size = 50),
        'loai_xe': fields.char( 'Loại xe',size = 50),
                }
phuong_tien()
class giay_phep(osv.osv):
    _name = "giay.phep"
    _columns = {
        'name': fields.char('Số giấy phép', size=10,required = True),
        'hang_gp': fields.char( 'Hạng',size = 10),
        'tuoc_hang': fields.char('Tước hạng',size = 50),
        'ngay_cap': fields.date('Ngày cấp'),
        'thoi_han': fields.date('Thời hạn'),
        'noi_cap_id': fields.many2one('thanh.pho', 'Nơi cấp'),
                }
giay_phep()
class doi_tuong_vp(osv.osv):
    _name = "doi.tuong.vp"
    _columns = {
        'name': fields.char('Tên người/Tổ chức VP', size=30,required = True),
        'ngay_sinh': fields.date('sinh_ngay'),
        'quoc_tich_id': fields.many2one('quoc.tich','Q.Tịch'),
        'ho_chieu': fields.char('CMND/Hộ chiếu',size = 50),
        'ngay_cap': fields.date('Ngày cấp'),
        'noi_cap_id': fields.many2one('thanh.pho','Nơi cấp'),
        'nghe_nghiep': fields.char('Nghề nghiệp',size = 50),
        'noi_o': fields.many2one('thanh.pho','Chỗ ở hiện nay'),
        'quan_huyen': fields.char(size = 50),
                }
doi_tuong_vp()
class quoc_tich(osv.osv):
    _name = "quoc.tich"
    _columns = {
        'name': fields.char('Tên Quốc Tịch',size = 50),
                }
quoc_tich()
class thanh_pho(osv.osv):
    _name = "thanh.pho"
    _columns = {
        'name': fields.char('Tên Thành Phố',size = 50),
                }
thanh_pho()
class ten_duong(osv.osv):
    _name = "ten.duong"
    _columns = {
        'name': fields.char('Tên Đường',size = 50),
                }
ten_duong()
class bien_ban(osv.osv):
    _name = "bien.ban"
    def onchange_vi_pham(self, cr, uid, ids, ma_loi=False, context=None):
        vals = {}
        if ma_loi:
            obj = self.pool.get('vi.pham').browse(cr, uid, ma_loi)
            vals = {'nd_loi':obj.noi_dung}
        return {'value': vals}
    def onchange_can_bo_lap(self, cr, uid, ids, can_bo_lap_id=False, context=None):
        vals = {}
        if can_bo_lap_id:
            obj = self.pool.get('can.bo').browse(cr, uid, can_bo_lap_id)
            vals = {'don_vi_id':obj.don_vi_id.id,'cap_bac':obj.cap_bac}
        return {'value': vals}

    def onchange_can_bo_qd(self, cr, uid, ids, can_bo_qd=False, context=None):
        vals = {}
        if can_bo_qd:
            obj = self.pool.get('can.bo').browse(cr, uid, can_bo_qd)
            vals = {'cap_ra_qd':obj.don_vi_id.id,'cap_bac_qd':obj.cap_bac,'chuc_vu_qd':obj.chuc_vu}
        return {'value': vals}
    def onchange_bien_so(self, cr, uid, ids, bien_so=False, context=None):
        vals = {}
        if bien_so:
            obj = self.pool.get('phuong.tien').browse(cr, uid, bien_so)
            vals = {'loai_xe':obj.loai_xe,'nhan_hieu':obj.nhan_hieu}
        return {'value': vals}
    def onchange_giay_phep(self, cr, uid, ids, so_gp_id=False, context=None):
        vals = {}
        if so_gp_id:
            obj = self.pool.get('giay.phep').browse(cr, uid, so_gp_id)
            vals = {
                    'hang_gp':obj.hang_gp,
                    'tuoc_hang':obj.tuoc_hang,
                    'ngay_cap_gp':obj.ngay_cap,
                    'thoi_han_gp':obj.thoi_han,
                    'noi_cap_gp':obj.noi_cap_id.id,
                    }
        return {'value': vals}
    def onchange_lap_luc(self, cr, uid, ids, lap_luc=False, context=None):#lap_luc: ten biến
        vals = {}
        if lap_luc:
            vals = {'vp_luc':lap_luc}
        return {'value': vals}
    def onchange_lap_ngay(self, cr, uid, ids, lap_ngay=False, context=None):
        vals = {}
        if lap_ngay:
            vals = {'vp_ngay':lap_ngay}
        return {'value': vals}
    def onchange_lap_tai(self, cr, uid, ids, lap_tai=False, context=None):
        vals = {}
        if lap_tai:
            vals = {'vp_tai':lap_tai}
        return {'value': vals}
    def onchange_lap_duong(self, cr, uid, ids, lap_duong=False, context=None):
        vals = {}
        if lap_duong:
            vals = {'vp_duong':lap_duong}
        return {'value': vals}
    def onchange_doi_tuong_vp(self, cr, uid, ids, ten_vp=False, context=None):
        vp = {}
        if ten_vp:
            obj = self.pool.get('doi.tuong.vp').browse(cr, uid, ten_vp)
            vp = {
                 'sinh_ngay':obj.ngay_sinh,
                 'cmnd_hc':obj.ho_chieu,
                 'ngay_ccmnd':obj.ngay_cap,
                 'noi_cmnd':obj.noi_cap_id.id,
                 'nghe_nghiep':obj.nghe_nghiep,
                 'noi_o':obj.noi_o.id,
                 'quan_huyen':obj.quan_huyen,
                 'quoc_tich_id':obj.quoc_tich_id.id,
                 }
        return {'value': vp}
    def create(self, cr, uid, vals, context=None):
        if vals.get('bien_so',False):
            obj = self.pool.get('phuong.tien').browse(cr, uid, vals['bien_so'])
            vals.update({'loai_xe':obj.loai_xe,'nhan_hieu':obj.nhan_hieu})
        if vals.get('so_gp_id',False):
            obj = self.pool.get('giay.phep').browse(cr, uid, vals['so_gp_id'])
            vals.update({
                    'hang_gp':obj.hang_gp,
                    'tuoc_hang':obj.tuoc_hang,
                    'ngay_cap_gp':obj.ngay_cap,
                    'thoi_han_gp':obj.thoi_han,
                    'noi_cap_gp':obj.noi_cap_id.id,
                    })
        if vals.get('ten_vp',False):
            obj = self.pool.get('doi.tuong.vp').browse(cr, uid, vals['ten_vp'])
            vals.update({
                         'sinh_ngay':obj.ngay_sinh,
                         'cmnd_hc':obj.ho_chieu,
                         'ngay_ccmnd':obj.ngay_cap,
                         'noi_cmnd':obj.noi_cap_id.id,
                         'nghe_nghiep':obj.nghe_nghiep,
                         'noi_o':obj.noi_o.id,
                         'quan_huyen':obj.quan_huyen,
                         'quoc_tich_id':obj.quoc_tich_id.id,
                         })
        if vals.get('can_bo_lap_id',False):
            obj = self.pool.get('can.bo').browse(cr, uid, vals['can_bo_lap_id'])
            vals.update({'don_vi_id': obj.don_vi_id.id,'cap_bac':obj.cap_bac})
        if vals.get('can_bo_qd',False):
            obj = self.pool.get('can.bo').browse(cr, uid, vals['can_bo_qd'])
            vals.update({'cap_ra_qd': obj.don_vi_id.id,'cap_bac_qd':obj.cap_bac,'chuc_vu_qd':obj.chuc_vu})
        return super(bien_ban, self).create(cr, uid, vals, context)
    def write(self, cr, uid, ids, vals, context=None, check=True, update_check=True):
        if vals.get('bien_so',False):
            obj = self.pool.get('phuong.tien').browse(cr, uid, vals['bien_so'])
            vals.update({'loai_xe':obj.loai_xe,'nhan_hieu':obj.nhan_hieu})
        if vals.get('so_gp_id',False):
            obj = self.pool.get('giay.phep').browse(cr, uid, vals['so_gp_id'])
            vals.update({
                    'hang_gp':obj.hang_gp,
                    'tuoc_hang':obj.tuoc_hang,
                    'ngay_cap_gp':obj.ngay_cap,
                    'thoi_han_gp':obj.thoi_han,
                    'noi_cap_gp':obj.noi_cap_id.id,
                    })
        if vals.get('ten_vp',False):
            obj = self.pool.get('doi.tuong.vp').browse(cr, uid, vals['ten_vp'])
            vals.update({
                         'sinh_ngay':obj.ngay_sinh,
                         'cmnd_hc':obj.ho_chieu,
                         'ngay_ccmnd':obj.ngay_cap,
                         'noi_cmnd':obj.noi_cap_id.id,
                         'nghe_nghiep':obj.nghe_nghiep,
                         'noi_o':obj.noi_o.id,
                         'quan_huyen':obj.quan_huyen,
                         'quoc_tich_id':obj.quoc_tich_id.id,
                         })
        if vals.get('can_bo_lap_id',False):
            obj = self.pool.get('can.bo').browse(cr, uid, vals['can_bo_lap_id'])
            vals.update({'don_vi_id': obj.don_vi_id.id,'cap_bac':obj.cap_bac})
        if vals.get('can_bo_qd',False):
            obj = self.pool.get('can.bo').browse(cr, uid, vals['can_bo_qd'])
            vals.update({'cap_ra_qd': obj.don_vi_id.id,'cap_bac_qd':obj.cap_bac,'chuc_vu_qd':obj.chuc_vu})
        return super(bien_ban, self).write(cr, uid, ids, vals, context)
    _columns = {
#         'check1': fields.boolean('check_onchange'),
        'don_vi_id': fields.many2one( 'don.vi','Đơn vị', readonly=True),
        'quyen_bb': fields.char( 'Quyển BB',size = 50,required = True),
        'so_bb': fields.char('Số BB', size=30,required = True),
        'can_bo_lap_id': fields.many2one( 'can.bo','Cán Bộ Lập'),
        'cap_bac':fields.char( 'Cấp bậc',size = 50, readonly=True),
        'lap_luc': fields.float( 'Lập Vào Lúc'),
        'lap_ngay': fields.date( 'Ngày',size = 50),
        'lap_tai': fields.char( 'Tại',size = 50),
        'lap_duong': fields.many2one( 'ten.duong','Đường'),
        'vp_luc': fields.float( 'VP Vào Lúc'),
        'vp_ngay': fields.date( 'Ngày',size = 50),
        'vp_tai': fields.char( 'Tại',size = 50),
        'vp_duong': fields.many2one( 'ten.duong','Đường'),
        'ten_vp': fields.many2one( 'doi.tuong.vp','Tên Người/Tổ Chức VP',required = True),
        'sinh_ngay': fields.char( 'Sinh Ngày', readonly=True),
        'quoc_tich_id': fields.many2one('quoc.tich','Q.Tịch', readonly=True),
        'cmnd_hc': fields.char( 'CMND/Hộ Chiếu',size = 50, readonly=True),
        'ngay_ccmnd': fields.char( 'Ngày Cấp',size = 50, readonly=True),
        'noi_cmnd': fields.many2one('thanh.pho','Nơi cấp', readonly=True),
        'nghe_nghiep': fields.char( 'Nghề Nghiệp',size = 50, readonly=True),
        'noi_o': fields.many2one('thanh.pho','Chỗ Ở Hiện Nay',readonly=True),
         'quan_huyen': fields.char(size = 50, readonly=True),
        'bien_so': fields.many2one( 'phuong.tien','PT Mang Biển Số'),
        'loai_xe': fields.char( 'Loại Xe',size = 50, readonly=True),
        'nhan_hieu': fields.char( 'Nhãn Hiệu',size = 50, readonly=True),
        'nghi_dinh': fields.many2one('nghi.dinh','Nghị Định'),
        'nd_nghi_dinh': fields.char('Nội Dung', size = 50),
        'ma_loi': fields.many2one('vi.pham', 'Mã Lỗi'),
        'nd_loi': fields.char( 'Nội Dung',size = 50),
        'vi_pham_id': fields.one2many('vi.pham','vi_pham_id'),
        'nag_nhe': fields.selection((('a','Tăng Nặng'), ('b','Giảm Nhẹ')),'Tăng Nặng/Giảm Nhẹ'),
        'tong_tien':fields.float('Tổng Tiền', readonly=True),
        'hoi_lo': fields.char( 'Nhập Tiền Hối Lộ',size = 50),
        'hinh_phat': fields.char( 'Hình Phạt',size = 50),
        'tam_giu': fields.many2one('tam.giu','Tạm Giữ'),
        'ngay_bd_tuoc': fields.date( 'Ngày BD Tước',size = 50),
        'so_gp_id': fields.many2one('giay.phep','Số GP'),
        'hang_gp': fields.char( 'Hạng',size = 50),
        'tuoc_hang': fields.char( 'Tước Hạng',size = 50),
        'ngay_cap_gp': fields.date( 'Ngày cấp',size = 50),
        'thoi_han_gp': fields.date( 'Thời Hạn',size = 50),
        'noi_cap_gp': fields.many2one('thanh.pho', 'Nơi cấp'),
        'nd_tam_giu': fields.text( 'Nội Dung Tạm Giữ'),
        'bo_sung': fields.text( 'Phạt Bổ Sung'),
        'ngan_chan': fields.text( 'Biện Pháp Ngăn Chăn'),
        'thoi_han_hq': fields.date( 'Th.Hạn KP Hậu Quả'),
        'kinh_phi_hq': fields.char( 'Kinh Phí KP Hậu Quả',size = 50),
        'in_tra_giay_to': fields.char( 'In Trả Giấy Tờ',size = 50),
        'cap_ra_qd': fields.many2one('don.vi','Cấp Ra QD',readonly=True),
        'can_bo_qd': fields.many2one( 'can.bo','In Cán Bộ Ra QD'),
        'cap_bac_qd': fields.char( 'Cấp Bậc',size = 50, readonly=True),
        'chuc_vu_qd': fields.char( 'Chức Vụ',size = 50, readonly=True),
        'so_bien_lai': fields.char( 'Số Biên Lai KB',size = 50),
        'ngay_dong_phat': fields.date( 'Ngày Đóng Phạt'),
        'ngay_ktll': fields.date( 'Ngày KTLL'),
        'ngay_ra_qd': fields.date( 'Ngày Ra QD'),
                }
bien_ban()

    