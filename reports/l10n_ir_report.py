from odoo import models, api


class InvoiceBlankFormat(models.AbstractModel):
    _name = 'report.l10n_ir.invoice_official_with_table_print'
    _description = 'Blank Invoice Template for Printing'

    @api.model
    def _get_report_values(self, docids, data=None):
        doc = type('doc', (), {})()
        doc.state = 'done'
        doc.company_id = self.env.user.company_id
        return {'doc': doc,
                'data': data,
                'doc_ids': docids}
