# from odoo.addons.jalali_calendar import jadatetime as jd

from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.company.account_tax_periodicity = 'trimester'
