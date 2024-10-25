# -*- coding: utf-8 -*-
import json
from odoo import http, _
from odoo.exceptions import UserError
from odoo.http import Response, request
import jwt
from datetime import datetime, timedelta

cors_headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Cache-Control": "no-store",
    "Pragma": "no-cache"
}


class LoginController(http.Controller):

    @http.route('/login', auth='public', type='http', csrf=False, methods=['POST'])
    def loginService(self, **kw):
        try:
            required_fields = ['login', 'password']
            for field in required_fields:
                if field not in kw or not kw.get(field):
                    return self._error_response("Falta el campo '{}' o está vacío.".format(field))

            login = kw['login']
            password = kw['password']

            user = request.env['res.users'].sudo().search(
                [('login', '=', login), ('password', '=', password)], limit=1)

            if user:
                try:
                    request.session.authenticate(
                        request.session.db, login, password)
                    session_token = request.session.sid
                    
                    expiration_time = datetime.utcnow() + timedelta(hours=1)

                    user_data = {
                        'token': request.session.sid,
                        'user_id': user.id,
                        'rol': user.rol_id.name,
                        'exp': expiration_time
                    }
                    
                    JWT_SECRET = 'F3n1xI0T'
                    JWT_ALGORITHM = 'HS256'
                    

                    token = jwt.encode(user_data, JWT_SECRET, algorithm=JWT_ALGORITHM)

                    response_data = self._success_response(
                        "Token Generado", token)
                    return Response(
                        status=200,
                        content_type="application/json; charset=utf-8",
                        headers={
                            "Access-Control-Allow-Origin": "*",
                            "Access-Control-Allow-Methods": "POST",
                            "Access-Control-Allow-Headers": "Content-Type",
                            "Cache-Control": "no-store",
                            "Pragma": "no-cache"
                        },
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
        except Exception as e:
            return self._error_response("Error al buscar el registro: {}".format(str(e)))

    def _success_response(self, message, data):
        return ({'success': True, 'message': message, 'data': data})

    def _error_response(self, error):
        return json.dumps({'success': False, 'error': error})
