# -*- coding: utf-8 -*-

from . import models
from . import wizard
from . import reports

def _account_tax_periodicity_set(env):
    env.company.account_tax_periodicity = 'trimester'
