import csv
import io
import logging
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from datetime import datetime, date
from odoo import http
from odoo.addons.web.controllers.export import CSVExport

_logger = logging.getLogger(__name__)

# Preserve original methods
original_init = getattr(CSVExport, '__init__', None)
original_from_data = CSVExport.from_data

# Patched __init__ method
def patched_init(self, *args, **kwargs):
    if original_init:
        original_init(self, *args, **kwargs)
    user_lang = getattr(http.request.env.user, 'lang', 'en_US') if http.request else 'en_US'
    self.is_persian = isinstance(user_lang, str) and user_lang.startswith('fa')
    _logger.debug(f"CSV Export initialized. Is Persian: {self.is_persian}")

# Patched from_data method
def patched_from_data(self, fields, columns_headers, rows):
    def convert_date_to_jalali(d):
        if isinstance(d, date) and not isinstance(d, datetime):
            return JalaliDate(d).strftime('%Y/%m/%d')
        elif isinstance(d, datetime):
            return JalaliDateTime(d).strftime('%Y/%m/%d %H:%M:%S')
        return d

    fp = io.StringIO()
    writer = csv.writer(fp, quoting=csv.QUOTE_MINIMAL)

    # Write headers
    writer.writerow(columns_headers)

    # Process rows
    rows = rows or []
    for data in rows:
        row = []
        for d in data:
            if d is None or d is False:
                d = ''
            elif isinstance(d, bytes):
                d = d.decode()
            if self.is_persian:
                d = convert_date_to_jalali(d)
            if isinstance(d, str) and d.startswith(('=', '-', '+')):
                d = "'" + d
            row.append(d)
        writer.writerow(row)

    return fp.getvalue()

# Apply patches
CSVExport.__init__ = patched_init
CSVExport.from_data = patched_from_data
