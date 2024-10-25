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


class Device_TypeController(http.Controller):
    @http.route('/createDeviceType', auth='public', type='http', csrf=False, methods=['POST'])
    def CreateDeviceTypeService(self, **kw):

        try:
            required_fields = ['name', 'proveedor', 'modelo', 'id']
            for field in required_fields:
                if field not in kw or not kw.get(field):
                    return self._error_response("Falta el campo '{}' o está vacío.".format(field))

                try:
                    user = request.env['res.users'].sudo().search(
                        [('id', '=', kw['id'])])

                    model = request.env['device.type.model'].with_user(user.id).create({
                        'name': kw['name'],
                        'proveedor': kw['proveedor'],
                        'modelo': kw['modelo'],
                    })

                    response_data = self._success_response(
                        "Registro Creado con Exito. Id: {}".format(model.id), model.id)

                    return Response(
                        status=200,
                        content_type="application/json; charset=utf-8",
                        headers=[(key, value)
                                 for key, value in cors_headers.items()],
                        response=json.dumps(response_data)
                    )

                except Exception as e:
                    response = self._error_response(
                        "Error al crear al realizar la operación: {}".format(str(e)))
                    return Response(
                        status=404,
                        content_type="application/json; charset=utf-8",
                        headers={
                            "Access-Control-Allow-Origin": "*",
                            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                            "Access-Control-Allow-Headers": "Content-Type",
                            "Cache-Control": "no-store",
                            "Pragma": "no-cache"
                        },
                        response=json.dumps(response)
                    )
        except Exception as e:
            return self._error_response("Error al buscar el registro: {}".format(str(e)))

    @http.route('/getDeviceType', auth='public', type='http', csrf=False, methods=['GET'])
    def GetDeviceTypeService(self, **kw):
        try:

            models = request.env['device.type.model'].sudo().search([])
            models_list = []

            if models:
                for model in models:

                    vals = {
                        'name': model.name,
                        'proveedor': model.proveedor,
                        'modelo': model.modelo,
                    }
                    models_list.append(vals)

            return Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers=[(key, value) for key, value in cors_headers.items()],
                response=json.dumps(models_list)
            )

        except Exception as e:
            response = self._error_response(
                "Error al crear al realizar la operación: {}".format(str(e)))
            return Response(
                status=404,
                content_type="application/json; charset=utf-8",
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Cache-Control": "no-store",
                    "Pragma": "no-cache"
                },
                response=json.dumps(response)
            )

    @http.route('/getDeviceTypewithFormat', auth='public', type='http', csrf=False, methods=['GET'])
    def GetDeviceTypewithFormatService(self, **kw):
        try:
            vehicules = request.env['device.type.model'].sudo().search([])
            vehicule_list = []

            if vehicules:
                for vehicule in vehicules:

                    vals = {
                        'name': vehicule.name + " " + vehicule.modelo + " " + vehicule.proveedor,
                        'value': vehicule.id
                    }
                    vehicule_list.append(vals)

            return Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers=[(key, value) for key, value in cors_headers.items()],
                response=json.dumps(vehicule_list)
            )

        except Exception as e:
            response = self._error_response(
                "Error al crear al realizar la operación: {}".format(str(e)))
            return Response(
                status=404,
                content_type="application/json; charset=utf-8",
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Cache-Control": "no-store",
                    "Pragma": "no-cache"
                },
                response=json.dumps(response)
            )

    @http.route('/updateDeviceType', auth='public', type='http', csrf=False, methods=['PUT'])
    def UpdateVehiculeService(self, **kw):
        try:
            requests = request.httprequest.data.decode()
            data = json.loads(requests)
            model = request.env['device.type.model'].sudo().search(
                [('id', '=', data.get('id'))])
            model_data = data.get('device')
            if not model:
                return self._error_response("El registro no existe.")

            if not model_data:
                return self._error_response("Datos no identificados.")

            try:
                required_fields = ['name', 'modelo', 'proveedor']
                for field in required_fields:
                    if field not in model_data or not model_data.get(field):
                        return self._error_response("Falta el campo '{}' o está vacío.".format(field))
            except Exception as e:
                return self._error_response("Error al guardar el registro: {}".format(str(e)))

            if model_data:
                try:
                    model.write(model_data)
                    response_data = self._success_response(
                        'Actualizacion de Datos', model.id)
                    return Response(
                        status=200,
                        content_type="application/json; charset=utf-8",
                        headers=[(key, value)
                                 for key, value in cors_headers.items()],
                        response=json.dumps(response_data)
                    )
                except Exception as e:
                    response = self._error_response(
                        "Error al crear al realizar la operación: {}".format(str(e)))
                    return Response(
                        status=404,
                        content_type="application/json; charset=utf-8",
                        headers={
                            "Access-Control-Allow-Origin": "*",
                            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                            "Access-Control-Allow-Headers": "Content-Type",
                            "Cache-Control": "no-store",
                            "Pragma": "no-cache"
                        },
                        response=json.dumps(response)
                    )

        except Exception as e:
            return self._error_response("Error al guardar el registro: {}".format(str(e)))

    def _success_response(self, message, data):
        return ({'success': True, 'message': message, 'data': data})

    def _error_response(self, error):
        return json.dumps({'success': False, 'error': error})
