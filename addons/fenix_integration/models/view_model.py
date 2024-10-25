from odoo import models, fields, api


class Views_Model(models.Model):

    _name = "views.model"
    _inherit = "mail.thread"
    _description = "Vistas Plataforma"

    active = fields.Boolean('Activo', default=True)
    state = fields.Selection([('draft', 'Borrador'), ('unavailable', 'Desactivado'), (
        'available', 'Disponible')], default="draft", string="Estado", tracking=True)
    name = fields.Char("Nombre")
    rol_id = fields.Many2one('roles.model', string="Rol Asignado", domain=[
                             ('active', '=', True)])
    url = fields.Char("Ruta")
    icon = fields.Char("Icono")
    position = fields.Integer(string="No. Posición", required=True)
