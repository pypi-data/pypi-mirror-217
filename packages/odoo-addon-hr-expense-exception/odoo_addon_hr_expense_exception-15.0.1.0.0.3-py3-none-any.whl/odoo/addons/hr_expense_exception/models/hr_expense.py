# Copyright 2021 Ecosoft <http://ecosoft.co.th>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HRExpense(models.Model):
    _inherit = ["hr.expense", "base.exception.method"]
    _name = "hr.expense"

    ignore_exception = fields.Boolean(
        related="sheet_id.ignore_exception", store=True, string="Ignore Exceptions"
    )

    def _get_main_records(self):
        return self.mapped("sheet_id")

    @api.model
    def _reverse_field(self):
        return "expense_sheet_ids"

    def _detect_exceptions(self, rule):
        records = super()._detect_exceptions(rule)
        return records.mapped("sheet_id")
