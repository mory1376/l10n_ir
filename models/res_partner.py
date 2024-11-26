from odoo import models, fields, exceptions

class ResPartner(models.Model):
    _inherit = 'res.partner'

    national_id_num = fields.Char(string="National ID Number", index=True)
    company_registry = fields.Char(string="Company Registry", index=True)

    _sql_constraints = [
        ('unique_national_id_num', 'unique(national_id_num)', 'The National ID Number must be unique!'),
        ('unique_company_registry', 'unique(company_registry)', 'The Company Registry must be unique!'),
    ]

