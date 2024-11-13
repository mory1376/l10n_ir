# qweb_field_converters.py
import re

from markupsafe import Markup

from odoo import api, fields, models, _
from odoo.tools import format_date, float_utils
from persiantools.jdatetime import JalaliDate, JalaliDateTime

class JalaliDateConverter(models.AbstractModel):
    _inherit = 'ir.qweb.field.date'

    @api.model
    def value_to_html(self, value, options):
        user_lang = self.user_lang()
        if user_lang.code == 'fa_IR' and value:  # Check if Persian is set
            # Convert to Jalali Date
            jalali_date = JalaliDate.to_jalali(value)
            # If 'format' is provided, use it; otherwise, use '%Y/%m/%d'
            jalali_format = options.get('format') if options.get('format') else '%Y/%m/%d'
            return jalali_date.strftime(jalali_format)

        # Otherwise, use the standard format
        return super(JalaliDateConverter, self).value_to_html(value, options)

class JalaliDateTimeConverter(models.AbstractModel):
    _inherit = 'ir.qweb.field.datetime'

    @api.model
    def value_to_html(self, value, options):
        user_lang = self.user_lang()
        if user_lang.code == 'fa_IR' and value:  # Check if Persian is set
            # Convert to Jalali DateTime
            jalali_datetime = JalaliDateTime.to_jalali(value)

            # Determine the format based on options
            if options.get('time_only'):
                jalali_format = '%H:%M:%S' if not options.get('hide_seconds') else '%H:%M'
            elif options.get('date_only'):
                jalali_format = '%Y/%m/%d'
            else:
                jalali_format = '%Y/%m/%d %H:%M:%S' if not options.get('hide_seconds') else '%Y/%m/%d %H:%M'

            # Override with custom format if provided
            if 'format' in options:
                jalali_format = options['format']

            # Format to string
            return jalali_datetime.strftime(jalali_format)

        # Otherwise, use the standard format
        return super(JalaliDateTimeConverter, self).value_to_html(value, options)

class MonetaryConverter(models.AbstractModel):
    _inherit = 'ir.qweb.field.monetary'

    @api.model
    def value_to_html(self, value, options):
        display_currency = options['display_currency']

        if not isinstance(value, (int, float)):
            raise ValueError(_("The value send to monetary field is not a number."))

        # lang.format mandates a sprintf-style format. These formats are non-
        # minimal (they have a default fixed precision instead), and
        # lang.format will not set one by default. currency.round will not
        # provide one either. So we need to generate a precision value
        # (integer > 0) from the currency's rounding (a float generally < 1.0).
        fmt = "%.{0}f".format(options.get('decimal_places', display_currency.decimal_places))

        if options.get('from_currency'):
            date = options.get('date') or fields.Date.today()
            company_id = options.get('company_id')
            if company_id:
                company = self.env['res.company'].browse(company_id)
            else:
                company = self.env.company
            value = options['from_currency']._convert(value, display_currency, company, date)

        lang = self.user_lang()
        formatted_amount = lang.format(fmt, display_currency.round(value), grouping=True)\
            .replace(r' ', '\N{NO-BREAK SPACE}').replace(r'-', '-\N{ZERO WIDTH NO-BREAK SPACE}')
        if display_currency.name == 'IRR':
            formatted_amount = formatted_amount.split('.')[0]

        pre = post = ''
        if display_currency.position == 'before':
            pre = '{symbol}\N{NO-BREAK SPACE}'.format(symbol=display_currency.symbol or '')
        else:
            post = '\N{NO-BREAK SPACE}{symbol}'.format(symbol=display_currency.symbol or '')

        if options.get('label_price') and lang.decimal_point in formatted_amount:
            sep = lang.decimal_point
            integer_part, decimal_part = formatted_amount.split(sep)
            integer_part += sep
            return Markup('{pre}<span class="oe_currency_value">{0}</span><span class="oe_currency_value" style="font-size:0.5em">{1}</span>{post}').format(integer_part, decimal_part, pre=pre, post=post)

        return Markup('{pre}<span class="oe_currency_value">{0}</span>{post}').format(formatted_amount, pre=pre, post=post)




