from persiantools.jdatetime import JalaliDate, JalaliDateTime
from datetime import datetime, date
from odoo import _, http
from odoo.addons.web.controllers.export import GroupExportXlsxWriter  # Import the correct class

# Preserve the original `__init__` method, if it exists
original_init = GroupExportXlsxWriter.__init__ if hasattr(GroupExportXlsxWriter, '__init__') else None

# Define the patched `__init__` method to set `is_persian`
def patched_init(self, *args, **kwargs):
    if original_init:
        original_init(self, *args, **kwargs)

    # Check if the user's language is Persian
    user_lang = http.request.env.user.lang if http.request else 'en_US'
    self.is_persian = user_lang.startswith('fa')

# Apply the monkey patch to `__init__`
GroupExportXlsxWriter.__init__ = patched_init

# Preserve the original `_write_group_header` method
original_write_group_header = GroupExportXlsxWriter._write_group_header

# Define the patched `_write_group_header` method
def patched_write_group_header(self, row, column, label, group, group_depth=0):
    # Convert label to Jalali if it's a date and `is_persian` is True
    if self.is_persian and isinstance(label, (date, datetime)):
        if isinstance(label, datetime):
            label = JalaliDateTime(label).strftime('%Y/%m/%d %H:%M:%S')
        else:
            label = JalaliDate(label).strftime('%Y/%m/%d')

    aggregates = group.aggregated_values
    label = '%s%s (%s)' % ('    ' * group_depth, label, group.count)
    self.write(row, column, label, self.header_bold_style)

    for field in self.fields[1:]:  # Skip first column to allow space for the group title
        column += 1
        aggregated_value = aggregates.get(field['name'])
        header_style = self.header_bold_style

        # Convert aggregated values to Jalali if `is_persian` and if value is date/datetime
        if self.is_persian and (field['type'] == 'date' or field['type'] == 'datetime'):
            if field['type'] == 'datetime':
                aggregated_value = JalaliDateTime(aggregated_value).strftime('%Y/%m/%d %H:%M:%S')
            else:
                aggregated_value = JalaliDate(aggregated_value).strftime('%Y/%m/%d')

        # Set the appropriate style based on field type
        if field['type'] == 'monetary':
            header_style = self.header_bold_style_monetary
        elif field['type'] == 'float':
            header_style = self.header_bold_style_float
        else:
            aggregated_value = str(aggregated_value if aggregated_value is not None else '')

        # Write the aggregated value
        self.write(row, column, aggregated_value, header_style)

    return row + 1, 0

# Apply the monkey patch to `_write_group_header`
GroupExportXlsxWriter._write_group_header = patched_write_group_header
