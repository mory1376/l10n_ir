from persiantools.jdatetime import JalaliDate, JalaliDateTime
from datetime import datetime, date
from odoo import _, http
from odoo.addons.web.controllers.export import ExportXlsxWriter # Import the original class
from odoo.exceptions import UserError

# Preserve the original `__init__` method
original_init = ExportXlsxWriter.__init__

# Define the patched `__init__` method
def patched_init(self, fields, columns_headers, row_count):
    # Call the original `__init__`
    original_init(self, fields, columns_headers, row_count)

    # Check if the user's language is Persian and set `is_persian` accordingly
    user_lang = http.request.env.user.lang if http.request else 'en_US'
    self.is_persian = user_lang.startswith('fa')

# Apply the monkey patch to `__init__`
ExportXlsxWriter.__init__ = patched_init

# Preserve the original `write_cell` method
original_write_cell = ExportXlsxWriter.write_cell

# Define the patched `write_cell` method
def patched_write_cell(self, row, column, cell_value):
    cell_style = self.base_style

    if isinstance(cell_value, bytes):
        try:
            cell_value = cell_value.decode()
        except UnicodeDecodeError:
            raise UserError(_("Binary fields cannot be exported to Excel unless base64-encoded."))

    elif isinstance(cell_value, (list, tuple, dict)):
        cell_value = str(cell_value)

    # Apply Jalali date conversion if `is_persian` is True
    if self.is_persian:
        if isinstance(cell_value, date) and not isinstance(cell_value, datetime):
            # Convert Date to Jalali
            cell_value = JalaliDate(cell_value).strftime('%Y/%m/%d')
            cell_style = self.date_style
        elif isinstance(cell_value, datetime):
            # Convert DateTime to Jalali
            cell_value = JalaliDateTime(cell_value).strftime('%Y/%m/%d %H:%M:%S')
            cell_style = self.datetime_style
    else:
        # Apply the original styles for non-Persian dates
        if isinstance(cell_value, datetime):
            cell_style = self.datetime_style
        elif isinstance(cell_value, date):
            cell_style = self.date_style
        elif isinstance(cell_value, float):
            field = self.fields[column]
            cell_style = self.monetary_style if field['type'] == 'monetary' else self.float_style

    if isinstance(cell_value, str) and len(cell_value) > self.worksheet.xls_strmax:
        cell_value = _("The content of this cell is too long for an XLSX file. Please use the CSV format for this export.")

    # Write the cell with the appropriate style
    self.write(row, column, cell_value, cell_style)

# Monkey-patch the `write_cell` method in `ExportXlsxWriter`
ExportXlsxWriter.write_cell = patched_write_cell
