from odoo import models, fields, api

class Roles_Model(models.Model):

    _name = "roles.model"
    _inherit = "mail.thread"
    _description = "Roles de Usuario"

    active = fields.Boolean('Activo', default=True)
    name = fields.Char("Nombre")
