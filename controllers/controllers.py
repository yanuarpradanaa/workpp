# -*- coding: utf-8 -*-
from odoo import http

# class Workpp(http.Controller):
#     @http.route('/workpp/workpp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/workpp/workpp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('workpp.listing', {
#             'root': '/workpp/workpp',
#             'objects': http.request.env['workpp.workpp'].search([]),
#         })

#     @http.route('/workpp/workpp/objects/<model("workpp.workpp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('workpp.object', {
#             'object': obj
#         })