from odoo import models,fields,api,_
from datetime import timedelta, datetime
from odoo.exceptions import UserError

class FormulariosColumnaConectada(models.Model):
    _inherit = "project.task"
    
    partner_type_vat = fields.Char(related='partner_id.l10n_latam_identification_type_id.name', readonly=True)
    partner_number_vat = fields.Char(related='partner_id.vat', readonly=True)
    sale_order_date = fields.Datetime(related='sale_order_id.date_order', readonly=True)
    
