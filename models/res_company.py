from odoo import models, fields

JALALI_MONTH_SELECTION = [
    ('1', 'Farvardin'),
    ('2', 'Ordibehesht'),
    ('3', 'Khordad'),
    ('4', 'Tir'),
    ('5', 'Mordad'),
    ('6', 'Shahrivar'),
    ('7', 'Mehr'),
    ('8', 'Aban'),
    ('9', 'Azar'),
    ('10', 'Dey'),
    ('11', 'Bahman'),
    ('12', 'Esfand'),
]


class ResCompany(models.Model):
    _inherit = "res.company"

    invoice_paper = fields.Selection([
        ('blank', 'Blank'),
        ('only series number printed', 'Only series number printed'),
        ('pre-printed', 'Pre-printed')],
        default='blank',
    )

    jalali_fiscalyear_last_day = fields.Integer(
        default=29,
        required=True,
    )
    jalali_fiscalyear_last_month = fields.Selection(
        selection=JALALI_MONTH_SELECTION,
        default="12",
        required=True,
    )
