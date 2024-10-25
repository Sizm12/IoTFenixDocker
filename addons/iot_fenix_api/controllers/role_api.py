# -*- coding: utf-8 -*-
import json
from odoo import http, _
from odoo.exceptions import UserError
from odoo.http import Response, request

cors_headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Cache-Control": "no-store",
    "Pragma": "no-cache"
}


class RoleController(http.Controller):

    @http.route('/getRoles', auth='public', type='http', csrf=False, methods=['GET'])
    def GetCategoriesService(self, **kw):
        try:
            roles = request.env['roles.model'].sudo().search([])
            roles_list = []

            if roles:
                for rol in roles:

                    vals = {
                        'id': rol.id,
                        'name': rol.name
                    }
                    roles_list.append(vals)

            return Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers=[(key, value) for key, value in cors_headers.items()],
                response=json.dumps(roles_list)
            )

        except Exception as e:
            response = self._error_response(
                "Error al crear al realizar la operación: {}".format(str(e)))
            return Response(
                status=404,
                content_type="application/json; charset=utf-8",
                headers=[(key, value)
                         for key, value in cors_headers.items()],
                response=json.dumps(response)
            )

    def _success_response(self, message, data):
        return ({'success': True, 'message': message, 'data': data})

    def _error_response(self, error):
        return json.dumps({'success': False, 'error': error})
