from datetime import date, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from persiantools.jdatetime import JalaliDate


class FinancialYearOpeningWizard(models.TransientModel):
    _inherit = 'account.financial.year.op'

    jalali_fiscalyear_last_day = fields.Integer(
        related="company_id.jalali_fiscalyear_last_day",
        readonly=False,
        help="The last day of the Jalali month will be used if the chosen day doesn't exist."
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
        related="company_id.jalali_fiscalyear_last_month",
        readonly=False,
    )
    is_persian_language = fields.Boolean(
        compute='_compute_is_persian_language',
        string="Is Persian Language",
    )

    @api.depends('company_id')
    def _compute_is_persian_language(self):
        """Determine if the user's language is Persian."""
        for record in self:
            user_lang = self.env.user.lang or 'en_US'
            record.is_persian_language = user_lang.startswith('fa')

    @api.constrains('jalali_fiscalyear_last_day', 'jalali_fiscalyear_last_month')
    def _check_jalali_fiscalyear_last_day(self):
        """Validate Jalali fiscal year last day based on the month and leap year status."""
        for record in self:
            if record.jalali_fiscalyear_last_month and record.jalali_fiscalyear_last_day:
                month = int(record.jalali_fiscalyear_last_month)
                day = record.jalali_fiscalyear_last_day
                current_year = JalaliDate.today().year

                # Define days per month
                days_in_month = {
                    1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31,
                    7: 30, 8: 30, 9: 30, 10: 30, 11: 30, 12: 29
                }

                # Check Esfand for leap year
                if month == 12:
                    is_leap_year = JalaliDate(current_year, 1, 1).isleap
                    max_days = 30 if is_leap_year else 29
                else:
                    max_days = days_in_month[month]

                if not (1 <= day <= max_days):
                    raise ValidationError(_(
                        "Invalid Jalali day '%s' for the month '%s'. The allowed range is 1-%s."
                        % (day, record.jalali_fiscalyear_last_month, max_days)
                    ))

    def write(self, vals):
        """
        Extend the write method to handle both Jalali and Gregorian fiscal year fields.
        """
        for wizard in self:
            update_vals = {
                'fiscalyear_last_day': vals.get('fiscalyear_last_day', wizard.company_id.fiscalyear_last_day),
                'fiscalyear_last_month': vals.get('fiscalyear_last_month', wizard.company_id.fiscalyear_last_month),
                'jalali_fiscalyear_last_day': vals.get('jalali_fiscalyear_last_day', wizard.company_id.jalali_fiscalyear_last_day),
                'jalali_fiscalyear_last_month': vals.get('jalali_fiscalyear_last_month', wizard.company_id.jalali_fiscalyear_last_month),
                'account_opening_date': vals.get('opening_date', wizard.company_id.account_opening_date),
            }
            # Update Gregorian fields
            if not wizard.is_persian_language:
                wizard.company_id.write({
                    'fiscalyear_last_day': update_vals['fiscalyear_last_day'],
                    'fiscalyear_last_month': update_vals['fiscalyear_last_month'],
                })

            # Update Jalali fields
            if wizard.is_persian_language:
                wizard.company_id.write({
                    'jalali_fiscalyear_last_day': update_vals['jalali_fiscalyear_last_day'],
                    'jalali_fiscalyear_last_month': update_vals['jalali_fiscalyear_last_month'],
                })

            # Update account opening move
            wizard.company_id.account_opening_move_id.write({
                'date': fields.Date.from_string(update_vals['account_opening_date']) - timedelta(days=1),
            })

        vals.pop('fiscalyear_last_day', None)
        vals.pop('fiscalyear_last_month', None)
        vals.pop('jalali_fiscalyear_last_day', None)
        vals.pop('jalali_fiscalyear_last_month', None)
        vals.pop('opening_date', None)

        return super().write(vals)
