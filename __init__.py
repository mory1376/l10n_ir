# -*- coding: utf-8 -*-

from . import models
from . import wizard
from . import reports


from odoo import api, SUPERUSER_ID


def _account_tax_periodicity_set(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.company.account_tax_periodicity = 'trimester'
