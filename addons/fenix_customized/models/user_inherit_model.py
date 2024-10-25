# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class user_inherit(models.Model):
    _inherit = 'res.users'

    rol_id = fields.Many2one('roles.model', string="Rol Plataforma", domain=[('active', '=', True)], tracking=True)