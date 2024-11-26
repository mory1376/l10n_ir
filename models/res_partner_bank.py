from odoo.addons.base_iban.models.res_partner_bank import _map_iban_template

# Extend or modify the global IBAN template variable
_map_iban_template.update({
    'ir': 'IRkk BBBB CCCC CCCC CCCC CCCC CCCC CCCC',  # Example for Iran
})
