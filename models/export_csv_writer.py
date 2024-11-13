import csv
import io
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from datetime import datetime, date
from odoo import _, http
from odoo.addons.web.controllers.export import CSVExport  # Import the original CSVExport class

# Preserve the original `__init__` method, if there is one
original_init = CSVExport.__init__ if hasattr(CSVExport, '__init__') else None


# Define the patched `__init__` method to set `is_persian`
def patched_init(self, *args, **kwargs):
    if original_init:
        original_init(self, *args, **kwargs)

    # Determine if the user's language is Persian
    user_lang = http.request.env.user.lang if http.request else 'en_US'
    self.is_persian = user_lang.startswith('fa')


# Apply the monkey patch to `__init__`
CSVExport.__init__ = patched_init

# Preserve the original `from_data` method
original_from_data = CSVExport.from_data


# Define the patched `from_data` method
def patched_from_data(self, fields, columns_headers, rows):
    # Initialize StringIO and CSV writer
    fp = io.StringIO()
    writer = csv.writer(fp, quoting=csv.QUOTE_MINIMAL)

    # Write headers
    writer.writerow(columns_headers)

    # Process each row for Jalali date conversion if needed
    for data in rows:
        row = []
        for d in data:
            if d is None or d is False:
                d = ''
            elif isinstance(d, bytes):
                d = d.decode()

            # Convert dates to Jalali if `is_persian` is True
            if self.is_persian:
                if isinstance(d, date) and not isinstance(d, datetime):
                    d = JalaliDate(d).strftime('%Y/%m/%d')
                elif isinstance(d, datetime):
                    d = JalaliDateTime(d).strftime('%Y/%m/%d %H:%M:%S')

            # Handle potential formula strings in CSV cells
            if isinstance(d, str) and d.startswith(('=', '-', '+')):
                d = "'" + d

            row.append(d)

        writer.writerow(row)

    return fp.getvalue()


# Monkey-patch the `from_data` method in `CSVExport`
CSVExport.from_data = patched_from_data
