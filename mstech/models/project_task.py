from odoo import models,fields,api,_
from datetime import timedelta, datetime
from odoo.exceptions import UserError

class FormulariosColumnaConectada(models.Model):
    _inherit = "project.task"
    
    partner_type_vat = fields.Char(related='partner_id.l10n_latam_identification_type_id.name', readonly=True)
    partner_number_vat = fields.Char(related='partner_id.vat', readonly=True)
    sale_order_date = fields.Datetime(related='sale_order_id.date_order', readonly=True, string="Fecha Orden de Venta")
    
    parent_res_contact = fields.Char(related='partner_id.child_ids.name', readonly=True, string="Contacto relacionado")
    parent_contact_function = fields.Char(related='partner_id.child_ids.function', readonly=True, striing="Puesto contacto relacionado")
    partner_province = fields.Char(related='partner_id.state_id.name', readonly=True)
    
    create_function = fields.Char(related='create_uid.function', readonly=True)
    create_number_vat = fields.Char(related='create_uid.vat', readonly=True)
    create_type_vat = fields.Char(related='create_uid.l10n_latam_identification_type_id.name', readonly=True)

    timesheets_employee = fields.Many2one(related="timesheet_ids.employee_id")
    timesheets_employee_id = fields.Integer(related='timesheet_ids.employee_id.id', readonly=True)
    timesheets_employee_name = fields.Char(related='timesheet_ids.employee_id.name', readonly=True)
    timesheets_employee_number_ident = fields.Char(related='timesheet_ids.employee_id.identification_id', readonly=True)
    #timesheets_employee_type_vat = fields.Char(related='timesheet_ids.employee_id.l10n_latam_identification_type_id.name', readonly=True)
    timesheets_employee_function = fields.Char(related='timesheet_ids.employee_id.job_title', readonly=True)
    #
    #order_line_m2m = fields.Many2many('sale.order.line', relation='orde_line_proj', colum1='name', colum2='order_id', string='Pedido de orden de venta')
    #
    order_line_product = fields.Many2one(related="sale_line_id.product_id", readonly=False)
    order_line_product_desc = fields.Text(related="sale_line_id.product_id.description")
    description_conclusion = fields.Text(string="Conclusiones y Recomendaciones")
    
    employee_signature = fields.Binary(string="Firma de empleado")
    state_payment_invoice = fields.Selection(related='sale_order_id.invoice_ids.payment_state',string="Estado de Pago Factura" ,readonly=True)
    
    #herramientas_project = fields.Many2many('stock.picking.type', relation='project_task_herramientas_rel', column1='name', column2='location_id', string='Transferencia Interna de Materiales')
    move_interno = fields.Many2one('stock.picking', string = "Movimiento interno", domain="[('partner_id', '=', 'company_id.partner_id')]")
    
    #related_ids = fields.Many2many('mymodule.mainmodel', relation='mymodule_mainmodel_rel', column1='left', column2='right', string='Related instances')
    #mes_task = fields.Selection([(1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'), (9, 'Setiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre'), ], string='Month')
    foto_ids = fields.Many2many(comodel_name='ir.attachment', relation='project_task_fotos_ids', column1='task_id', column2='attachment_id', string='Fotos')
    
    sale_line_product = fields.Many2one('sale.order.line',string='Orden de linea')
    sale_line_product2 = fields.One2many('sale.order.line','project_order_line',string='Orden de linea 2')
    #@onchange('planned_date_begin')
    #def _onchange_mes_task(self):
    #    var = 0
    #    var = datetime.strptimr()
        
class PointofSale(models.Model):
    _inherit = 'product.product'
    
    @api.onchange('type')
    def _onchange_pos_ok(self):
        if self.type == 'product':
            self.available_in_pos = 1
        else:
            self.available_in_pos = 0

class SaleProject(models.Model):
    _inherit = "sale.order.line"
    project_order_line = fields.Many2one('project.task', string='Orden de Linea para Tareas')
