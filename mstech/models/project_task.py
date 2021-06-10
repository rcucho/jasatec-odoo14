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
    client_signature = fields.Binary(string="Firma del cliente")
    state_payment_invoice = fields.Selection(related='sale_order_id.invoice_ids.payment_state',string="Estado de Pago Factura" ,readonly=True)
    
    #herramientas_project = fields.Many2many('stock.picking.type', relation='project_task_herramientas_rel', column1='name', column2='location_id', string='Transferencia Interna de Materiales')
    move_interno = fields.Many2one('stock.picking', string = "Movimiento interno", domain="[('partner_id', '=', 'company_id.partner_id')]")
    
    #mes_task = fields.Selection([(1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'), (9, 'Setiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre'), ], string='Month')
    foto_ids = fields.Many2many(comodel_name='ir.attachment', relation='project_task_fotos_ids', column1='task_id', column2='attachment_id', string='Fotos')
    
    sale_line_product = fields.Many2one('sale.order.line',string='Orden de linea')
    sale_line_product2 = fields.One2many('sale.order.line','task_id',string='Orden de linea 2', compute='_compute_sale_line_product2')
    
    #sale_line_product3 = fields.One2many('sale.order', 'order_line', string="orden de linea")    
    sale_line_product3 = fields.One2many('sale.order','project_order_line',string='Orden de linea 3')
    sale_line_product4 = fields.One2many(related='sale_line_id.order_id.order_line',string='Orden de linea aaaa')
    
    sale_line_product5 = fields.Many2many(comodel_name='sale.order.line', relation='relation_task_product', column1='project_task_id', column2='sale_order_line_id', string ='Productos vendidos', compute='_compute_sale_line_product5')
    
    def _compute_sale_line_product2(self):
        sale_order = self.env['sale.order'].browse(self._context.get('active_ids', []))
        for record in self:
            tareas = record.project_id.task_ids
            linea = sale_order.order_line
            #linea = record.sale_line_id.order_id.order_line
            algo = linea.filtered(lambda ele: ele.id not in tareas.sale_line_id.ids)
            record.sale_line_product2 = algo
    
    def _compute_sale_line_product5(self):
        sale_order = self.env['sale.order'].browse(self._context.get('active_ids', []))
        for record in self:
            tareas = record.project_id.task_ids
            linea = sale_order.order_line
            #linea = record.sale_line_id.order_id.order_line
            algo = linea.filtered(lambda ele: ele.id not in tareas.sale_line_id.ids)
            record.sale_line_product5 = algo
        
class PointofSale(models.Model):
    _inherit = 'product.product'
    
    @api.onchange('type')
    def _onchange_pos_ok(self):
        if self.type == 'product':
            self.available_in_pos = 1
        else:
            self.available_in_pos = 0

class SaleProject(models.Model):
    #_inherit = "sale.order.line"
    _inherit = "sale.order"
    project_order_line = fields.Many2one('project.task', string='Orden de Linea para Tareas', compute="_compute_project_order")
    
    def _compute_project_order(self):
        for record in self:
            project_order_line = self.order_line
