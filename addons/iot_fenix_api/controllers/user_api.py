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


class UserController(http.Controller):

    @http.route('/createUser', auth='public', type='http', csrf=False, methods=['POST'])
    def CreateUserService(self, **kw):
        try:
            required_fields = ['username', 'email', 'password', 'rol_id']
            for field in required_fields:
                if field not in kw or not kw.get(field):
                    return self._error_response("Falta el campo '{}' o está vacío.".format(field))

            username = kw['username']
            email = kw['email']
            password = kw['password']
            rol = kw['rol_id']

            user = request.env['res.users'].sudo().create({
                'name': username,
                'login': email,
                'email': email,
                'password': password,
                'rol_id': rol
            })
            response_data = self._success_response(
                "Usuario Creado", user.id)

            return Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers=[(key, value) for key, value in cors_headers.items()],
                response=json.dumps(response_data)
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

    @http.route('/getUser', auth='public', type='http', csrf=False, methods=['GET'])
    def GetUserService(self, **kw):
        try:
            users = request.env['res.users'].sudo().search([])
            users_list = []

            if users:
                for user in users:
                    last_login = None
                    if user.login_date:
                        last_login = user.login_date.strftime(
                            '%Y-%m-%d %H:%M:%S')
                    vals = {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email,
                        'last_authentication': last_login,
                        'state': user.state
                    }
                    users_list.append(vals)

            return Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers=[(key, value) for key, value in cors_headers.items()],
                response=json.dumps(users_list)
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

    @http.route('/deleteUser', auth='public', type='http', csrf=False, methods=['DELETE'])
    def DeleteUserService(self, **kw):
        try:
            required_fields = ['id']
            for field in required_fields:
                if field not in kw or not kw.get(field):
                    return self._error_response("Falta el campo '{}' o está vacío.".format(field))

            idUser = int(kw['id'])

            if idUser:
                try:
                    request.env['res.users'].sudo().browse(idUser).unlink()
                    response_data = self._success_response(
                        "Usuario {} Eliminado" .format(idUser), idUser)
                    return Response(
                        status=200,
                        content_type="application/json; charset=utf-8",
                        headers=[(key, value)
                                 for key, value in cors_headers.items()],
                        response=json.dumps(response_data)
                    )
                except Exception as e:
                    return self._error_response(f"Error al borrar el Usuario {str(e)}")

        except Exception as e:
            return self._error_response("Error al guardar el registro: {}".format(str(e)))

    def _success_response(self, message, data):
        return ({'success': True, 'message': message, 'data': data})

    def _error_response(self, error):
        return json.dumps({'success': False, 'error': error})
