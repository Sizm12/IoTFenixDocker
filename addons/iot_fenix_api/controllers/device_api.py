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


class DeviceController(http.Controller):

    @http.route('/createDevice', auth='public', type='http', csrf=False, methods=['POST'])
    def CreateFleetService(self, **kw):
        try:
            required_fields = ['flespi_id', 'name', 'imei', 'fecha_obtencion',
                               'device_type', 'id']
            for field in required_fields:
                if field not in kw or not kw.get(field):
                    return self._error_response("Falta el campo '{}' o está vacío.".format(field))

                try:
                    user = request.env['res.users'].sudo().search(
                        [('id', '=', kw['id'])])
                    model = request.env['devices.model'].with_user(user.id).create({
                        'name': kw['name'],
                        'flespi_id': kw['flespi_id'],
                        'imei': kw['imei'],
                        'fecha_obtencion': kw['fecha_obtencion'],
                        'device_type': kw['device_type'],
                    })

                    response_data = self._success_response(
                        "Dispositivo Creado con Exito. Id: {}".format(model.id), model.id)

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

    @http.route('/getDevice', auth='public', type='http', csrf=False, methods=['GET'])
    def GetVehiculesService(self, **kw):
        try:

            required_fields = ['id']
            for field in required_fields:
                if field not in kw or not kw.get(field):
                    return self._error_response("Falta el campo '{}' o está vacío.".format(field))

            models = request.env['devices.model'].sudo().search(
                [('create_uid.id', '=', kw['id'])])
            models_list = []

            if models:
                for model in models:
                    date = None
                    if model.fecha_obtencion:
                        date = model.fecha_obtencion.strftime('%Y-%m-%d')

                    vals = {
                        'id': model.id,
                        'name': model.name,
                        'imei': model.imei,
                        'fecha_obtencion': date,
                        'device_type_id': model.device_type.id,
                        'device_type_name': model.device_type.name,
                        'flespi_id': model.flespi_id,
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

    @http.route('/getDevicewithFormat', auth='public', type='http', csrf=False, methods=['GET'])
    def GetVehiculewithFormatService(self, **kw):
        try:
            required_fields = ['id']
            for field in required_fields:
                if field not in kw or not kw.get(field):
                    return self._error_response("Falta el campo '{}' o está vacío.".format(field))

            vehicules = request.env['devices.model'].sudo().search(
                [('create_uid.id', '=', kw['id']), ('asignado', '=', False)])
            vehicule_list = []

            if vehicules:
                for vehicule in vehicules:

                    vals = {
                        'name': vehicule.name + " " + str(vehicule.device_type.name) + " " + vehicule.imei,
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

    @http.route('/updateDevice', auth='public', type='http', csrf=False, methods=['PUT'])
    def UpdateVehiculeService(self, **kw):
        try:
            requests = request.httprequest.data.decode()
            data = json.loads(requests)
            model = request.env['devices.model'].sudo().search(
                [('id', '=', data.get('id'))])
            model_data = data.get('device')
            if not model:
                return self._error_response("El registro no existe.")

            if not model_data:
                return self._error_response("Datos no identificados.")

            try:
                required_fields = ['name', 'imei',
                                   'fecha_obtencion', 'device_type', 'flespi_id']
                for field in required_fields:
                    if field not in model_data or not model_data.get(field):
                        return self._error_response("Falta el campo '{}' o está vacío.".format(field))
                if model_data:
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
