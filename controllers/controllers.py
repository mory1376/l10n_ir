# -*- coding: utf-8 -*-
# from odoo import http


# class L10nIr(http.Controller):
#     @http.route('/l10n_ir/l10n_ir', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10n_ir/l10n_ir/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10n_ir.listing', {
#             'root': '/l10n_ir/l10n_ir',
#             'objects': http.request.env['l10n_ir.l10n_ir'].search([]),
#         })

#     @http.route('/l10n_ir/l10n_ir/objects/<model("l10n_ir.l10n_ir"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10n_ir.object', {
#             'object': obj
#         })

