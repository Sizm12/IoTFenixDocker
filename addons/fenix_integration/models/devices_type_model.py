# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Device_Type(models.Model):

    _name = "device.type.model"
    _inherit = "mail.thread"
    _description = "Tipos de Dispositivos"

    active = fields.Boolean('Activo', default=True)
    name = fields.Char("Nombre")
    proveedor = fields.Char("Proveedor")
    modelo = fields.Char('Modelo')
    company_id = fields.Many2one('res.company', string='Empresa', default=lambda self: self.env.company)
