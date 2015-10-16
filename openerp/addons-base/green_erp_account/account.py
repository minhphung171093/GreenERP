# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2010-2012 OpenERP SA (<http://openerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import api, fields, models


class account_analytic_account(models.Model):
    _inherit = "account.analytic.account"

    @api.depends('line_ids.amount')
    def _compute_debit_credit_balance(self):
        analytic_line_obj = self.env['account.analytic.line']
        domain = [('account_id', 'in', self.mapped('id'))]
        if self._context.get('from_date', False):
            domain.append(('date', '>=', self._context['from_date']))
        if self._context.get('to_date', False):
            domain.append(('date', '<=', self._context['to_date']))

        account_amounts = analytic_line_obj.search_read(domain, ['account_id', 'amount'])
        account_ids = set([line['account_id'][0] for line in account_amounts])
        data_debit = {account_id: 0.0 for account_id in account_ids}
        data_credit = {account_id: 0.0 for account_id in account_ids}
        for account_amount in account_amounts:
            if account_amount['amount'] < 0.0:
                data_debit[account_amount['account_id'][0]] += account_amount['amount']
            else:
                data_credit[account_amount['account_id'][0]] += account_amount['amount']

        for account in self:
            account.update({
                'debit': abs(data_debit.get(account.id, 0.0)),
                'credit': data_credit.get(account.id, 0.0),
                'balance': data_credit.get(account.id, 0.0) - abs(data_debit.get(account.id, 0.0))
            })
    
    balance = fields.Monetary(compute='_compute_debit_credit_balance', string='Balance', store=True)
    debit = fields.Monetary(compute='_compute_debit_credit_balance', string='Debit', store=True)
    credit = fields.Monetary(compute='_compute_debit_credit_balance', string='Credit', store=True)
    percent = fields.Float('Percent')
    parent_company_id = fields.Many2one(related='company_id.parent_id', string='Parent Company',store=True,readonly=True)
    
account_analytic_account()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: