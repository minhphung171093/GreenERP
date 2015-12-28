# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class product_template(osv.osv):
    _inherit = 'product.template'

    _columns = {
        'test_ckeditor': fields.text('Test CK'),
    }
