from odoo import models,fields,api,_
from odoo.exceptions import UserError

class FormulariosColumnaConectada(models.Model):
    _inherit = "project.task"
    
    hola_g = fields.Char(string="Hola")