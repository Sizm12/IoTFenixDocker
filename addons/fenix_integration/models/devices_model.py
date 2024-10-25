# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Devices_Model(models.Model):

    _name = "devices.model"
    _inherit = "mail.thread"
    _description = "Dispositivos IOT"

    state = fields.Selection([('draft', 'Borrador'), ('unavailable','Desactivado'), ('available','Disponible')], default="draft", string="Estado", tracking=True)
    active = fields.Boolean('Activo', default=True)
    flespi_id= fields.Integer(string="Identificador", required=True)
    name= fields.Char("Nombre")
    imei = fields.Char("IMEI", required = True, tracking = True)
    fecha_obtencion = fields.Date(string="Fecha de Compra", tracking = True)
    device_type = fields.Many2one('device.type.model', string="Tipo de Dispositivo", domain=[('active', '=', True)])
    fleet_id = fields.Many2one('fleet.vehicle', string="Vehiculo")
    asignado = fields.Boolean('Asignado', default=False, tracking = True)
    company_id = fields.Many2one('res.company', string='Empresa', default=lambda self: self.env.company)


