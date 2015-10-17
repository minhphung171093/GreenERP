# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp.osv import fields, osv

class account_analytic_chart(osv.osv_memory):
    _inherit = 'account.analytic.chart'

    def analytic_account_chart_open_window(self, cr, uid, ids, context=None):
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        result_context = {}
        if context is None:
            context = {}
        result = mod_obj.get_object_reference(cr, uid, 'analytic', 'action_analytic_account_form')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        data = self.read(cr, uid, ids, [])[0]
        if data['from_date']:
            result_context.update({'from_date': data['from_date']})
        if data['to_date']:
            result_context.update({'to_date': data['to_date']})
        result_context.update({'search_default_company': True})
        result['context'] = str(result_context)
        return result
