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

    order_line_product = fields.Many2one(related="sale_line_id.product_id", readonly=False)
    order_line_product_desc = fields.Text(related="sale_line_id.product_id.description")
    description_conclusion = fields.Text(string="Conclusiones y Recomendaciones")
    
    employee_signature = fields.Binary(string="Firma de empleado")
    client_signature = fields.Binary(string="Firma del cliente")
    state_payment_invoice = fields.Selection(related='sale_order_id.invoice_ids.payment_state',string="Estado de Pago Factura" ,readonly=True)
    
    foto_ids = fields.Many2many(comodel_name='ir.attachment', relation='project_task_fotos_ids', column1='task_id', column2='attachment_id', string='Fotos')
    
    #sale_line_product4 = fields.One2many(related='sale_line_id.order_id.order_line',string='Orden de linea aaaa')
    #---------------------------------------------------------------------------------------------
    cliente_task = fields.Many2one('res.partner', string="Cliente de Tarea", compute="_onchange_cliente_task")
    sale_line_product = fields.Many2many(comodel_name='sale.order.line', relation='relation_task_product', column1='project_task_id', column2='sale_order_line_id', string ='Productos vendidos', compute='_compute_sale_line_product')
    fecha_inicio = fields.Date(string='Fecha de inicio de tarea', compute='_onchange_fecha_inicio')
    fecha_fin = fields.Date(string="Fecha fin de Tarea", compute='_onchange_fecha_fin')
    nombre_titulo = fields.Char(string="Titulo de Tarea", readonly=True, compute='_onchange_nombre_titulo')
    mov_herramienta = fields.Many2many(comodel_name='stock.picking', relation='relation_task_herramienta', column1='project_task_id', column2='stock_picking_id', 
                                       string='Herramientas')#, compute='_compute_mov_herramienta')
    task_picking = fields.One2many('stock.picking','picking_task', string="Herram.")#, compute = '_compute_task_picking', readonly=False)
    #---------------------------------------------------------------------------------------------
    
    def _compute_mov_herramienta(self):
        for record in self:
            record.mov_herramienta.partner_id = record.partner_id
            record.mov_herramienta.picking_type_id.code = 'internal'    
    
    @api.onchange('sale_line_id')
    def _compute_sale_line_product(self):
        #sale_order = self.env['sale.order'].browse(self._context.get('active_ids', []))
        for record in self:
            tareas = record.project_id.task_ids
            #linea = sale_order.order_line
            linea = record.sale_line_id.order_id.order_line
            algo = linea.filtered(lambda ele: ele.id not in tareas.sale_line_id.ids)
            record.sale_line_product = algo
    
    @api.onchange('partner_id')
    def _onchange_cliente_task(self):
        for record in self:
            #if record.cliente_task:
            record.cliente_task = record.partner_id
    
    @api.onchange('name')
    def _onchange_nombre_titulo(self):
        for record in self:
            #if record.nombre_titulo:
            record.nombre_titulo = record.name
            
    @api.onchange('planned_date_begin')
    def _onchange_fecha_inicio(self):
        for record in self:
            if record.planned_date_begin:
                record.fecha_inicio = record.planned_date_begin.strftime("%Y-%m-%d")
        
    @api.onchange('planned_date_end')
    def _onchange_fecha_fin(self):
        for record in self:
            if record.planned_date_end:
                record.fecha_fin = record.planned_date_end.strftime("%Y-%m-%d")
                

    def do_unreserve(self):
        for record in self:
            record.mov_herramienta.do_unreserve()
        return True
    
    def action_confirm(self):
        for record in self:
            record.task_picking.action_confirm()
        return True
    
    def action_assign(self):
        for record in self:
            record.task_picking.action_assign()
        return True
    
    def button_validate(self):
        for record in self:
            record.task_picking.button_validate()
        return True
        
    
    
class PointofSale(models.Model):
    _inherit = 'product.product'
    
    @api.onchange('type')
    def _onchange_pos_ok(self):
        if self.type == 'product':
            self.available_in_pos = 1
        else:
            self.available_in_pos = 0
            
class StockPickingTask(models.Model):
    _inherit = 'stock.picking'
    
    picking_task = fields.Many2one('project.task', string="tarea en movimiento")
    
    @api.model
    def create(self, vals):
        defaults = self.default_get(['name', 'picking_type_id'])
        picking_type = self.env['stock.picking.type'].browse(vals.get('picking_type_id', defaults.get('picking_type_id')))             
        if self.picking_task:
            if vals.get('name', '/') == '/' and defaults.get('name', '/') == '/' and vals.get('picking_type_id', defaults.get('picking_type_id')):
                vals['name'] = picking_type.sequence_id.next_by_id()
        res = super(StockPickingTask,self).create(vals)      
        return res
    
    @api.onchange('picking_type_id', 'partner_id')
    def onchange_picking_type(self):
        for record in self:
            if record.picking_task:
                record.picking_type_id = (5, 'San Francisco: Internal Transfers')
        picki = super().onchange_picking_type()
        return picki
    
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for record in self:
            if record.picking_task:
                record.partner_id = record.picking_task.partner_id
        parti = super().onchange_partner_id()
        return parti
    
    @api.depends('state', 'move_lines', 'move_lines.state', 'move_lines.package_level_id', 'move_lines.move_line_ids.package_level_id')
    def _compute_move_without_package(self):
        for record in self:
            if record.picking_task:
                movimi = record.move_ids_without_package
                herra = movimi.filtered(lambda x_h: x_h.movimi.product_id.categ_id.name == 'Herramientas')
                record.move_ids_without_package = herra        
        mov_he = super()._compute_move_without_package()
        return mov_he
    
    def validate_directo(self):
        for record in self:
            record.action_confirm()
            record.action_assign()
            if record.action_assign() == True:
                record.button_validate()
                #record.button_validate()
        return True
