# -*- coding: utf-8 -*-
##############################################################################
#
#    HLVSolution, Open Source Management Solution
#
##############################################################################

import openerp
from openerp.osv import osv, fields
from openerp.tools.translate import _

class res_groups(osv.osv):
    _inherit = "res.groups"
    
    _columns = {
        'greenerp': fields.boolean('GreenERP'),
    }
    
res_groups()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: