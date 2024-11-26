from collections import namedtuple

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from persiantools.jdatetime import JalaliDate


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_persian_language = fields.Boolean(
        compute='_compute_is_persian_language',
        string="Is Persian Language",
    )
    jalali_fiscalyear_last_day = fields.Integer(
        string="Jalali Last Day",
        related="company_id.jalali_fiscalyear_last_day",
        readonly=False
    )
    jalali_fiscalyear_last_month = fields.Selection(
        selection=[
            ('1', 'Farvardin'),
            ('2', 'Ordibehesht'),
            ('3', 'Khordad'),
            ('4', 'Tir'),
            ('5', 'Mordad'),
            ('6', 'Shahrivar'),
            ('7', 'Mehr'),
            ('8', 'Aban'),
            ('9', 'Azar'),
            ('10', 'Dey'),
            ('11', 'Bahman'),
            ('12', 'Esfand'),
        ],
        string="Jalali Last Month",
        related="company_id.jalali_fiscalyear_last_month",
        readonly=False
    )
    invoice_paper = fields.Selection(
        default='blank',
        related='company_id.invoice_paper',
        readonly=False,
    )

    def print_invoice(self):
        Doc = namedtuple('Doc', 'state company_id')
        return self.env.ref('l10n_ir.action_invoice_official_with_table_print').report_action(
            self.company_id, data={
                'doc': Doc('done', self.company_id)})

    @api.depends('company_id')
    def _compute_is_persian_language(self):
        """Determine if the user's language is Persian."""
        for record in self:
            user_lang = self.env.user.lang or 'en_US'
            record.is_persian_language = user_lang.startswith('fa')

    @api.model_create_multi
    def create(self, vals_list):
        """
        Handle the creation of settings while ensuring related fields
        for fiscalyear_last_day, fiscalyear_last_month,
        jalali_fiscalyear_last_day, and jalali_fiscalyear_last_month
        are saved correctly.
        """
        for vals in vals_list:
            fiscalyear_last_day = vals.pop('fiscalyear_last_day', False) or self.env.company.fiscalyear_last_day
            fiscalyear_last_month = vals.pop('fiscalyear_last_month', False) or self.env.company.fiscalyear_last_month
            jalali_last_day = vals.pop('jalali_fiscalyear_last_day', False) or self.env.company.jalali_fiscalyear_last_day
            jalali_last_month = vals.pop('jalali_fiscalyear_last_month', False) or self.env.company.jalali_fiscalyear_last_month

            update_vals = {}
            # Handle Jalali to Gregorian conversion
            if jalali_last_day and jalali_last_month:
                try:
                    current_jalali_year = JalaliDate.today().year
                    jalali_date = JalaliDate(
                        current_jalali_year,
                        int(jalali_last_month),
                        jalali_last_day
                    )
                    gregorian_date = jalali_date.to_gregorian()
                    fiscalyear_last_day = gregorian_date.day
                    fiscalyear_last_month = str(gregorian_date.month)
                except ValueError:
                    raise UserError(_("Invalid Jalali fiscal year day/month combination."))

            # Check if Gregorian fields need updating
            if fiscalyear_last_day != self.env.company.fiscalyear_last_day:
                update_vals['fiscalyear_last_day'] = fiscalyear_last_day
            if fiscalyear_last_month != self.env.company.fiscalyear_last_month:
                update_vals['fiscalyear_last_month'] = fiscalyear_last_month

            # Check if Jalali fields need updating
            if jalali_last_day != self.env.company.jalali_fiscalyear_last_day:
                update_vals['jalali_fiscalyear_last_day'] = jalali_last_day
            if jalali_last_month != self.env.company.jalali_fiscalyear_last_month:
                update_vals['jalali_fiscalyear_last_month'] = jalali_last_month

            # Write updates to the company
            if update_vals:
                self.env.company.write(update_vals)

        return super().create(vals_list)
