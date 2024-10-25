from odoo import models, fields, api

class Permissions_Model(models.Model):

    _name = "permissions.model"
    _inherit = "mail.thread"
    _description = "Permisos de Usuario"

    active = fields.Boolean('Activo', default=True)
    state = fields.Selection([('draft', 'Borrador'), ('unavailable','Desactivado'), ('available','Disponible')], default="draft", string="Estado", tracking=True)
    name = fields.Char("Nombre")