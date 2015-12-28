# -*- coding: utf-8 -*-
import base64

from openerp import SUPERUSER_ID
from openerp import http
from openerp.tools.translate import _
from openerp.http import request

from openerp.addons.website.models.website import slug

class green_erp_website_sale(http.Controller):
    @http.route([
        '/sales',
    ], type='http', auth="public", website=True)
    def sales(self, country=None, department=None, office_id=None):
        env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))
 
        Sales = env['sale.order']
 
        # List jobs available to current UID
        sale_ids = Sales.search([('user_id','=',request.uid)], order="website_published desc").ids
        # Browse jobs as superuser, because address is restricted
        sales = Sales.sudo().browse(sale_ids)
 
        # Render page
        return request.website.render("green_erp_website_sale.index", {
            'sales': sales,
        })
    @http.route('/sales/detail/<model("sale.order"):sale>', type='http', auth="public", website=True)
    def jobs_detail(self, sale, **kwargs):
        return request.render("green_erp_website_sale.detail", {
            'sale': sale,
            'main_object': sale,
        })

# vim :et:
