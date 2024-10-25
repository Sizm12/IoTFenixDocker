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


class ModelController(http.Controller):

    @http.route('/createModels', auth='public', type='http', csrf=False, methods=['POST'])
    def CreateModelsService(self, **kw):
        try:
            required_fields = ['name', 'brand_id', 'category_id', 'seats',
                               'doors', 'color', 'model_year', 'default_fuel_type', 'transmission', 'power', 'horsepower', 'id']
            for field in required_fields:
                if field not in kw or not kw.get(field):
                    return self._error_response("Falta el campo '{}' o está vacío.".format(field))

                try:
                    user = request.env['res.users'].sudo().search(
                        [('id', '=', kw['id'])])

                    model = request.env['fleet.vehicle.model'].with_user(user.id).create({
                        'name': kw['name'],
                        'brand_id': kw['brand_id'],
                        'category_id': kw['category_id'],
                        'seats': kw['seats'],
                        'doors': kw['doors'],
                        'color': kw['color'],
                        'model_year': kw['model_year'],
                        'default_fuel_type': kw['default_fuel_type'],
                        'transmission': kw['transmission'],
                        'power': kw['power'],
                        'horsepower': kw['horsepower'],
                    })

                    response_data = self._success_response(
                        "Modelo Creado con Exito. Id: {}".format(model.id), model.id)

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

    @http.route('/getModel', auth='public', type='http', csrf=False, methods=['GET'])
    def GetModelsService(self, **kw):
        try:

            required_fields = ['id']
            for field in required_fields:
                if field not in kw or not kw.get(field):
                    return self._error_response("Falta el campo '{}' o está vacío.".format(field))

            models = request.env['fleet.vehicle.model'].sudo().search(
                [('create_uid.id', '=', kw['id'])])
            models_list = []

            if models:
                for model in models:

                    vals = {
                        'name': model.name,
                        'brand_id': model.brand_id.id,
                        'brand_name': model.brand_id.name,
                        'category_id': model.category_id.id,
                        'category_name': model.category_id.name,
                        'seats': model.seats,
                        'doors': model.doors,
                        'color': model.color,
                        'model_year': model.model_year,
                        'default_fuel_type': model.default_fuel_type,
                        'transmission': model.transmission,
                        'power': model.power,
                        'horsepower': model.horsepower,
                    }
                    models_list.append(vals)

            return Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Cache-Control": "no-store",
                    "Pragma": "no-cache"
                },
                response=json.dumps(models_list)
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

    @http.route('/getModelwithFormat', auth='public', type='http', csrf=False, methods=['GET'])
    def GetModelswithFormatService(self, **kw):
        try:
            required_fields = ['id']
            for field in required_fields:
                if field not in kw or not kw.get(field):
                    return self._error_response("Falta el campo '{}' o está vacío.".format(field))

            vehicules = request.env['fleet.vehicle.model'].sudo().search(
                [('create_uid.id', '=', kw['id'])])
            vehicule_list = []

            if vehicules:
                for vehicule in vehicules:

                    vals = {
                        'name': vehicule.name + " " + vehicule.brand_id.name,
                        'value': vehicule.id
                    }
                    vehicule_list.append(vals)

            return Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Cache-Control": "no-store",
                    "Pragma": "no-cache"
                },
                response=json.dumps(vehicule_list)
            )

        except Exception as e:
            response = self._error_response(
                "Error al guardar el registro: {}".format(str(e)))
            return Response(
                status=404,
                content_type="application/json; charset=utf-8",
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Cache-Control": "no-store",
                    "Pragma": "no-cache"
                },
                response=json.dumps(response)
            )

    @http.route('/updateModel', auth='public', type='http', csrf=False, methods=['PUT'])
    def UpdateModelService(self, **kw):
        try:
            requests = request.httprequest.data.decode()
            data = json.loads(requests)
            model = request.env['fleet.vehicle.model'].sudo().search(
                [('id', '=', data.get('model_id'))])
            model_data = data.get('model')
            if not model:
                return self._error_response("El registro no existe.")

            if not model_data:
                return self._error_response("Datos no identificados.")

            try:
                required_fields = ['name', 'brand_id',
                                   'category_id', 'model_year', 'color']
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
