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


class FleetController(http.Controller):

    @http.route('/createFleet', auth='public', type='http', csrf=False, methods=['POST'])
    def CreateFleetService(self, **kw):
        try:
            required_fields = ['model_id', 'driver_id',
                               'license_plate', 'vin', 'device_id', 'id']
            for field in required_fields:
                if field not in kw or not kw.get(field):
                    return self._error_response("Falta el campo '{}' o está vacío.".format(field))

            search = http.request.env['fleet.vehicle'].sudo().search(
                [
                    ('model_id', '=', kw['model_id']),
                    ('license_plate', '=', kw['license_plate']),
                    ('device_id', '=', kw['device_id']),
                    ('vin', '=', kw['vin'])])

            if search:
                try:
                    data = []
                    for vehicule in search:
                        vals = {
                            'id': vehicule.id,
                            'name': vehicule.model_id.name,
                            'driver_id': vehicule.driver_id.name,
                            'license_plate': vehicule.license_plate,
                            'vin': vehicule.vin,
                            'device_id': vehicule.device_id.id + " " + vehicule.device_id.name,
                        }
                        data.append(vals)

                    response_data = self._success_response(
                        "Se ha encontrado información que coincide con los datos ingresados.", data)

                    return Response(
                        status=200,
                        content_type="application/json; charset=utf-8",
                        headers=[(key, value)
                                 for key, value in cors_headers.items()],
                        response=json.dumps(response_data)
                    )

                except Exception as e:
                    return self._error_response("Error al buscar el registro: {}".format(str(e)))

            else:
                try:
                    user = request.env['res.users'].sudo().search(
                        [('id', '=', kw['id'])])
                    vehicule = request.env['fleet.vehicle'].with_user(user.id).create({
                        'model_id': kw['model_id'],
                        'driver_id': kw['driver_id'],
                        'license_plate': kw['license_plate'],
                        'device_id': kw['device_id'],
                        'vin': kw['vin'],
                    })

                    response_data = self._success_response(
                        "Vehiculo Creado con Exito. Id: {}".format(vehicule.id), vehicule.id)

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
                        headers=[(key, value)
                                 for key, value in cors_headers.items()],
                        response=json.dumps(response)
                    )
        except Exception as e:
            return self._error_response("Error al buscar el registro: {}".format(str(e)))

    @http.route('/FindVehicule', auth='public', type='http', csrf=False, methods=['GET'])
    def FindVehiculeService(self, **kw):

        required_fields = ['license_plate']
        for field in required_fields:
            if field not in kw or not kw.get(field):
                return self._error_response("Falta el campo '{}' o está vacío.".format(field))

        try:
            vehicule = request.env['fleet.vehicle'].sudo().search(
                [('license_plate', '=', kw['license_plate'])])
            data = []

            if vehicule:
                for vehicule_data in vehicule:
                    vals = {
                        'id': vehicule_data.id,
                        'name': vehicule_data.model_id.name,
                        'driver': vehicule_data.driver_id.name,
                        'license_plate': vehicule_data.license_plate,
                        'vin': vehicule_data.vin,
                        'device_id': vehicule_data.device_id.id + " " + vehicule_data.device_id.name,
                    }
                    data.append(vals)
                response_data = self._success_response(
                    "Se ha encontrado el vehiculo Buscado.", data)

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
                headers=[(key, value)
                         for key, value in cors_headers.items()],
                response=json.dumps(response)
            )

    @http.route('/getVehicule', auth='public', type='http', csrf=False, methods=['GET'])
    def GetVehiculesService(self, **kw):
        try:

            required_fields = ['id']
            for field in required_fields:
                if field not in kw or not kw.get(field):
                    return self._error_response("Falta el campo '{}' o está vacío.".format(field))

            vehicules = request.env['fleet.vehicle'].sudo().search(
                [('create_uid.id', '=', kw['id'])])
            vehicule_list = []

            if vehicules:
                for vehicule in vehicules:

                    vals = {
                        'id': vehicule.id,
                        'vin': vehicule.vin,
                        'model_id': vehicule.model_id.id,
                        'model_name': vehicule.model_id.name,
                        'license_plate': vehicule.license_plate,
                        'driver_id': vehicule.driver_id.id,
                        'driver_name': vehicule.driver_id.name,
                        'device_id': vehicule.device_id.id,
                        'device_name': vehicule.device_id.name
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
                headers=[(key, value)
                         for key, value in cors_headers.items()],
                response=json.dumps(response)
            )

    @http.route('/getVehiculewithFormat', auth='public', type='http', csrf=False, methods=['GET'])
    def GetVehiculewithFormatService(self, **kw):
        try:
            required_fields = ['id']
            for field in required_fields:
                if field not in kw or not kw.get(field):
                    return self._error_response("Falta el campo '{}' o está vacío.".format(field))

            vehicules = request.env['fleet.vehicle'].sudo().search(
                [('create_uid.id', '=', kw['id'])])
            vehicule_list = []

            if vehicules:
                for vehicule in vehicules:

                    vals = {
                        'name': vehicule.model_id.name + " " + vehicule.license_plate,
                        'value': vehicule.device_id.id
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
                headers=[(key, value)
                         for key, value in cors_headers.items()],
                response=json.dumps(response)
            )

    @http.route('/disableVehicule', auth='public', type='http', csrf=False, methods=['PUT'])
    def DeleteVehiculeService(self, **kw):
        try:
            required_fields = ['id']
            for field in required_fields:
                if field not in kw or not kw.get(field):
                    return self._error_response("Falta el campo '{}' o está vacío.".format(field))

            idUser = int(kw['id'])

            if idUser:
                try:
                    vehicule = request.env['fleet.vehicle'].sudo().search(
                        [('id', '=', idUser)])
                    vehicule.write({
                        'active': False
                    })
                    response_data = self._success_response(
                        "Vehiculo {} Desactivado" .format(vehicule.id), vehicule.id)
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
                        headers=[(key, value)
                                 for key, value in cors_headers.items()],
                        response=json.dumps(response)
                    )

        except Exception as e:
            return self._error_response("Error al guardar el registro: {}".format(str(e)))

    @http.route('/updateVehicule', auth='public', type='http', csrf=False, methods=['PUT'])
    def UpdateVehiculeService(self, **kw):
        try:
            requests = request.httprequest.data.decode()
            data = json.loads(requests)
            vehicule_id = data.get('vehicule_id')
            vehicule = request.env['fleet.vehicle'].sudo().browse(vehicule_id)
            vehicule_data = data.get('vehicule')
            if not vehicule:
                return self._error_response("El registro no existe.")

            if not vehicule_data:
                return self._error_response("Datos no identificados.")

            try:
                required_fields = ['vin', 'device_id',
                                   'model_id', 'license_plate', 'driver_id']
                for field in required_fields:
                    if field not in vehicule_data or not vehicule_data.get(field):
                        return self._error_response("Falta el campo '{}' o está vacío.".format(field))

                if vehicule_data:
                    vehicule.write(vehicule_data)
                    response_data = self._success_response(
                        'Actualizacion de Datos', vehicule.id)
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
                    headers=[(key, value)
                             for key, value in cors_headers.items()],
                    response=json.dumps(response)
                )

        except Exception as e:
            return self._error_response("Error al guardar el registro: {}".format(str(e)))

    def _success_response(self, message, data):
        return ({'success': True, 'message': message, 'data': data})

    def _error_response(self, error):
        return json.dumps({'success': False, 'error': error})
