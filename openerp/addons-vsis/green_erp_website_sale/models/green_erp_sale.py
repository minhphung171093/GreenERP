# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class sale_order(osv.osv):
    _name = 'sale.order'
    _inherit = ['sale.order','website.seo.metadata']

    def _website_url(self, cr, uid, ids, field_name, arg, context=None):
        res = dict.fromkeys(ids, '')
        for sale in self.browse(cr, uid, ids, context=context):
            res[sale.id] = "/sales/detail/%s" % sale.id
        return res

    def sale_open(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'website_published': False}, context=context)
        return super(sale_order, self).sale_open(cr, uid, ids, context)

    _columns = {
        'website_published': fields.boolean('Published', copy=False),
        'website_description': fields.html('Website description'),
        'website_url': fields.function(_website_url, string="Website URL", type="char"),
    }
    _defaults = {
        'website_published': False
    }
