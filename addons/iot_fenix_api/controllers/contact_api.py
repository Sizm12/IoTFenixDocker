# -*- coding: utf-8 -*-
import json
from odoo import http, _
from odoo.exceptions import UserError
from odoo.http import Response, request
import logging

_logger = logging.getLogger(__name__)

cors_headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Cache-Control": "no-store",
    "Pragma": "no-cache"
}


class ContactController(http.Controller):

    @http.route('/createContact', auth='public', type='http', csrf=False, methods=['POST'])
    def CreateContactService(self, **kw):
        try:
            required_fields = ['name', 'vat', 'email', 'phone', 'id']
            for field in required_fields:
                if field not in kw or not kw.get(field):
                    return self._error_response("Falta el campo '{}' o está vacío.".format(field))

            search = http.request.env['res.partner'].sudo().search(
                [
                    ('name', '=', kw['name']),
                    ('vat', '=', kw['vat'])])

            if search:
                try:
                    data = []
                    for client_data in search:
                        vals = {
                            'id': client_data.id,
                            'name': client_data.name,
                            'street': client_data.street,
                            'street2': client_data.street2,
                            'city': client_data.city,
                            'vat': client_data.vat,
                            'email': client_data.email,
                            'phone': client_data.phone,
                            'company_type': client_data.company_type,
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
                    response = self._error_response(
                        "Error al buscar el registro: {}".format(str(e)))
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

            else:
                try:
                    user = request.env['res.users'].sudo().search(
                        [('id', '=', kw['id'])])
                    client = request.env['res.partner'].with_user(user.id).create({
                        'name': kw['name'],
                        'street': kw['street'],
                        'street2': kw['street2'],
                        'city': kw['city'],
                        'vat': kw['vat'],
                        'email': kw['email'],
                        'phone': kw['phone'],
                    })

                    response_data = self._success_response(
                        "Contacto Creado con Exito. Id: {}".format(client.id), client.id)

                    return Response(
                        status=200,
                        content_type="application/json; charset=utf-8",
                        headers=[(key, value)
                                 for key, value in cors_headers.items()],
                        response=json.dumps(response_data)
                    )

                except Exception as e:
                    _logger.exception("Error al crear el Cliente: %s", str(e))
                    response = self._error_response(
                        "Error al crear el Cliente: {}".format(str(e)))
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
            response = self._error_response(
                "Error al buscar el registro: {}".format(str(e)))
            return Response(
                status=404,
                content_type="application/json; charset=utf-8",
                headers=[(key, value) for key, value in cors_headers.items()],
                response=json.dumps(response)
            )

    @http.route('/FindContact', auth='public', type='http', csrf=False, methods=['GET'])
    def FindContactService(self, **kw):

        required_fields = ['name']
        for field in required_fields:
            if field not in kw or not kw.get(field):
                return self._error_response("Falta el campo '{}' o está vacío.".format(field))

        try:
            client = request.env['res.partner'].sudo().search(
                [('name', '=', kw['name'])])
            data = []

            if client:
                for client_data in client:
                    vals = {
                        'id': client_data.id,
                        'name': client_data.name,
                        'street': client_data.street,
                        'street2': client_data.street2,
                        'city': client_data.city,
                        'vat': client_data.vat,
                        'email': client_data.email,
                        'phone': client_data.phone,
                        'company_type': client_data.company_type,
                        'company_id': client_data.company_id.name
                    }
                    data.append(vals)
                response_data = self._success_response(
                    "Se ha encontrado al Cliente Buscado.", data)

                return Response(
                    status=200,
                    content_type="application/json; charset=utf-8",
                    headers=[(key, value)
                             for key, value in cors_headers.items()],
                    response=json.dumps(response_data)
                )
        except Exception as e:
            return self._error_response("Error al buscar el registro: {}".format(str(e)))

    @http.route('/getContactList', auth='public', type='http', csrf=False, methods=['GET'])
    def GetContactListService(self, **kw):
        try:
            contacts = request.env['res.partner'].sudo().search(
                [('create_uid.id', '=', kw['id']), ('active', '=', True)])
            contacts_list = []

            if contacts:
                for contact in contacts:
                    vals = {
                        'id': contact.id,
                        'name': contact.name,
                    }
                    contacts_list.append(vals)

            return Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers=[(key, value) for key, value in cors_headers.items()],
                response=json.dumps(contacts_list)
            )

        except Exception as e:
            response = self._error_response(
                "Error al guardar el registro: {}".format(str(e)))
            return Response(
                status=404,
                content_type="application/json; charset=utf-8",
                headers=[(key, value) for key, value in cors_headers.items()],
                response=json.dumps(response)
            )
    
    @http.route('/getContact', auth='public', type='http', csrf=False, methods=['GET'])
    def GetContactService(self, **kw):
        try:
            contacts = request.env['res.partner'].sudo().search(
                [('create_uid.id', '=', kw['id']), '|', ('active', '=', True), ('active', '=', False)])
            contacts_list = []

            if contacts:
                for contact in contacts:
                    address_parts = []

                    if contact.street is not None:
                        address_parts.append(str(contact.street))
                    if contact.street2 is not None:
                        address_parts.append(str(contact.street2))
                    if contact.city is not None:
                        address_parts.append(str(contact.city))

                    address = " ".join(address_parts)

                    vals = {
                        'id': contact.id,
                        'name': contact.name,
                        'email': contact.email,
                        'phone': contact.phone,
                        'vat': contact.vat,
                        'address': address,
                        'active': contact.active
                    }
                    contacts_list.append(vals)

            return Response(
                status=200,
                content_type="application/json; charset=utf-8",
                headers=[(key, value) for key, value in cors_headers.items()],
                response=json.dumps(contacts_list)
            )

        except Exception as e:
            response = self._error_response(
                "Error al guardar el registro: {}".format(str(e)))
            return Response(
                status=404,
                content_type="application/json; charset=utf-8",
                headers=[(key, value) for key, value in cors_headers.items()],
                response=json.dumps(response)
            )

    @http.route('/disableContact', auth='public', type='http', csrf=False, methods=['PUT'])
    def DisableUserService(self, **kw):
        try:
            required_fields = ['id']
            for field in required_fields:
                if field not in kw or not kw.get(field):
                    return self._error_response("Falta el campo '{}' o está vacío.".format(field))

            idUser = int(kw['id'])

            if idUser:
                try:
                    contact = request.env['res.partner'].sudo().search(
                        [('id', '=', idUser)])
                    contact.write({
                        'active': False
                    })

                    response_data = self._success_response(
                        "Usuario {} Desactivado" .format(contact.id), contact.id)
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

    @http.route('/updateContact', auth='public', type='http', csrf=False, methods=['PUT'])
    def UpdateCustomerService(self, **kw):
        try:
            requests = request.httprequest.data.decode()
            data = json.loads(requests)
            contact_id = data.get('contact_id')
            contact = request.env['res.partner'].sudo().browse(contact_id)
            contact_data = data.get('contact')
            if not contact:
                return self._error_response("El contacto no existe.")

            if not contact_data:
                return self._error_response("Datos no identificados.")

            try:
                required_fields = ['name', 'street', 'street2',
                                   'city', 'vat', 'email', 'phone']
                for field in required_fields:
                    if field not in contact_data or not contact_data.get(field):
                        return self._error_response("Falta el campo '{}' o está vacío.".format(field))

                if contact_data:
                    contact.write(contact_data)
                    response_data = self._success_response(
                        'Actualizacion de Datos', contact.id)
                    return Response(
                        status=200,
                        content_type="application/json; charset=utf-8",
                        headers=[(key, value)
                                 for key, value in cors_headers.items()],
                        response=json.dumps(response_data)
                    )
            except Exception as e:
                response = self._error_response(
                    "Error al realizar la operación: {}".format(str(e)))
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
