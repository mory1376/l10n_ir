from odoo import models, api, fields, _
from odoo.exceptions import UserError  # Import UserError for other exceptions
from odoo.addons.base_import.models.base_import import ImportValidationError  # Correct import

import jdatetime  # Importing jdatetime at the top

class ImportJalaliDate(models.TransientModel):
    _inherit = 'base_import.import'

    @api.model
    def _parse_date_from_data(self, data, index, name, field_type, options):
        user_lang = self.env.user.lang
        # Check if the user's language is Persian (fa_IR)
        if user_lang and user_lang.startswith('fa'):
            fmt = fields.Date.to_string if field_type == 'date' else fields.Datetime.to_string

            # Define supported Jalali date formats
            date_formats = [
                '%Y/%m/%d',
                '%Y-%m-%d',
                '%Y/%-m/%-d',
                '%Y-%-m-%-d',
            ]

            datetime_formats = [
                '%Y/%m/%d %H:%M:%S',
                '%Y-%m-%d %H:%M:%S',
                '%Y/%-m/%-d %H:%M:%S',
                '%Y-%-m-%-d %H:%M:%S',
                '%Y/%m/%d %H:%M',
                '%Y-%m-%d %H:%M',
                '%Y/%-m/%-d %H:%M',
                '%Y-%-m-%-d %H:%M',
            ]

            for num, line in enumerate(data):
                date_str = line[index].strip()
                if not date_str:
                    continue

                # Choose appropriate formats based on field type
                formats_to_try = date_formats if field_type == 'date' else datetime_formats

                for date_format in formats_to_try:
                    try:
                        # Parse Jalali date
                        if field_type == 'date':
                            jalali_date = jdatetime.datetime.strptime(date_str, date_format).date()
                            # Convert to Gregorian date
                            gregorian_date = jalali_date.togregorian()
                            line[index] = fmt(gregorian_date)
                            break  # Date parsed successfully
                        elif field_type == 'datetime':
                            jalali_datetime = jdatetime.datetime.strptime(date_str, date_format)
                            # Convert to Gregorian datetime
                            gregorian_datetime = jalali_datetime.togregorian()
                            line[index] = fmt(gregorian_datetime)
                            break  # Datetime parsed successfully
                    except (ValueError, TypeError):
                        continue  # Try the next date format
                else:
                    # No date format matched
                    raise ImportValidationError(
                        _("Column '%(column)s' contains incorrect values. Error on line %(line)d: Unable to parse date '%(value)s' with supported Jalali date formats.",
                          column=name, line=num + 1, value=date_str),
                        field=name,
                        field_type=field_type
                    )
        else:
            # Default behavior for other languages
            super(ImportJalaliDate, self)._parse_date_from_data(data, index, name, field_type, options)
