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


class ManufacturerController(http.Controller):

    @http.route('/createManufacturer', auth='public', type='http', csrf=False, methods=['POST'])
    def CreateCategoryService(self, **kw):
        try:
            required_fields = ['name']
            for field in required_fields:
                if field not in kw or not kw.get(field):
                    return self._error_response("Falta el campo '{}' o está vacío.".format(field))

                try:
                    model = request.env['fleet.vehicle.model.brand'].sudo().create({
                        'name': kw['name'],
                    })

                    response_data = self._success_response(
                        "Categoria Creada con Exito. Id: {}".format(model.id), model.id)

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

    @http.route('/getManufacturer', auth='public', type='http', csrf=False, methods=['GET'])
    def GetCategoriesService(self, **kw):
        try:
            models = request.env['fleet.vehicle.model.brand'].sudo().search([])
            models_list = []

            if models:
                for model in models:

                    vals = {
                        'id': model.id,
                        'name': model.name
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
                headers=[(key, value)
                         for key, value in cors_headers.items()],
                response=json.dumps(response)
            )

    def _success_response(self, message, data):
        return ({'success': True, 'message': message, 'data': data})

    def _error_response(self, error):
        return json.dumps({'success': False, 'error': error})
