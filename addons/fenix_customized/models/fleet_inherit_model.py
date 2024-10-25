# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class fleet_inherit(models.Model):
    _inherit = 'fleet.vehicle'

    device_id = fields.Many2one('devices.model', string="Dispositivo Asociado", domain=[('asignado', '=', False)], tracking=True)
    vin = fields.Char(string="VIN", tracking=True)
    image = fields.Binary(string="Imagen")

    @api.onchange('device_id')
    def OnChangeDevice(self):
        if self.device_id:
            self.device_id.asignado = True

    def unlink(self):
        for record in self:
            if record.device_id:
                record.device_id.asignado = False
        return super(fleet_inherit, self).unlink()
