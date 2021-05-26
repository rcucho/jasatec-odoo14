from odoo import models,fields,api,_
from odoo.exceptions import UserError

class FormulariosColumnaConectada(models.Model):
    _inherit = "project.task"
    
    hola_g = fields.Char(string="Hola")
    partner_type_vat = fields.Char(related='partner_id.l10n_latam_identification_type_id.name', readonly=True)
    partner_number_vat = fields.Char(related='partner_id.vat', readonly=True)
