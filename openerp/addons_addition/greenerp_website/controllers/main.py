# -*- coding: utf-8 -*-
import base64

from openerp import SUPERUSER_ID
from openerp import http
from openerp.tools.translate import _
from openerp.http import request

from openerp.addons.website.models.website import slug

class greenerp_website(http.Controller):

    @http.route([
        '/farm',
    ], type='http', auth="public", website=True)
    def hello(self):
        return request.website.render("greenerp_website.index")
    
    @http.route([
        '/category',
    ], type='http', auth="public", website=True)
    def go_to_category(self):
        env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))
 
        Products = env['product.product']
 
        # List jobs available to current UID
        product_ids = Products.search([], order="website_published desc").ids
        # Browse jobs as superuser, because address is restricted
        products = Products.sudo().browse(product_ids)
        return request.website.render("greenerp_website.category",{
                       'products':products,     
                                                                   })

# vim :et:
