from odoo import models, fields,api,_
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class MealOrder(models.Model):
    _name="meal.order"
    _description="Meal Order"
    _order="name"


    def customer_domain(self):
        customers = self.env['res.partner'].search([('is_company', '=', True)])

        return [('id', 'in', customers.ids)]

    name = fields.Char("Name", required=True, copy=False,
                       default=lambda self: _("New")) #default="NEW"

    customer_id = fields.Many2one('res.partner',string="Customer",
                                domain=customer_domain) #[('is_company','=',True)]
    is_urgent = fields.Boolean("Is Urgent", copy=False)
    total_price = fields.Float("Total", readonly=True,
                               compute="_compute_total_price", store=True,
                              ) # groups="tech_order.tech_order_mgr"
    order_type = fields.Selection([('internal','Internal'),('external','External')],
                                  string="Type", deafult='internal')
    note = fields.Text("Note", translate=True)
    table_number = fields.Integer("Table Number")
    expected_duration = fields.Float("Expected Duration")
    order_date = fields.Date("Order Date", default=fields.datetime.now().date(),
                             required=True, copy=False)
    expected_date = fields.Datetime("Expected Date", compute="_compute_expected_date",
                                     readonly=False,
                                    inverse="inverse_expected_date")
    active = fields.Boolean("Active", default=True)
    tag_ids = fields.Many2many("order.tag", string="Tags"
                             )
    item_ids = fields.One2many('order.item', 'order_id', string='Items')
    external_item_ids = fields.Many2many('external.item', string="External Items")
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('in_process', 'In Process'),
                              ('delivered', 'Delivered'),
                              ('cancelled', 'Cancelled'),
                              ],
                             string="State", default='draft')


    _sql_constraints = [('name_uniq', 'unique (name)', "Order Name already exists!")]


    @api.constrains('order_date')
    def check_order_date(self):
        if self.order_date > datetime.now().date():
            raise ValidationError("Stop")

    @api.constrains('table_number')
    def check_table_number(self):
        max_table_number = self.env['ir.config_parameter'].sudo().get_param('tech_order.max_table_number')
        if self.table_number > int(max_table_number):
            raise ValidationError("Max Table Number is " + str(max_table_number))


    @api.depends('item_ids.total_price')
    def _compute_total_price(self):
        for record in self:
            record.total_price = sum(record.item_ids.mapped('total_price'))
            # sum([500, 700, 800])

    @api.depends('order_date', 'expected_duration')
    def _compute_expected_date(self):
        for record in self:
            record.expected_date = record.order_date + timedelta(
                days=record.expected_duration)

    def inverse_expected_date(self):
        for record in self:
            record.expected_duration = (record.expected_date.date() - record.order_date).days

    # @api.model_create_multi
    # def create(self, vals_list):
    #     [{},{}]

    @api.model
        #object.m_name() --> m_name(object == self)
        #self.env['order.meal'].m_name()
    def create(self, vals): #vals = {}
        _logger.error("vals +++ " + str(vals))
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('order_meal_name_seq')
        return super().create(vals)

    # @api.model
    # def create(self, vals):  # vals = {}
    #     result = super().create(vals)
    #     result.name = self.env['ir.sequence'].next_by_code('order_meal_name_seq')
    #     return result




    def action_confirm(self):
        if self.state == 'draft':
            self.state = 'confirmed'

    def action_in_process(self):
        if self.state == 'confirmed':
            self.state = 'in_process'

    def action_delivered(self):
        self.state = 'delivered'
        self.customer_id.update({'customer_rank': self.customer_id.customer_rank + 1})

    def action_cancelled(self):
        _logger.error(" CONTXT " + str(self.env.context.get("cancelled_value")))
        self.state = 'cancelled'

    def check_urgent(self):
        for order in self:
            expected_date = order.expected_date.date() - timedelta(days=1)
            if expected_date == datetime.now().date():
                order.is_urgent = True


    def fetch_order(self):
        # state in (confirmed, in_process)
        # AND
        # (
        # external and expected_date > current date
        # OR
        # internal and table_umber == 0
        # )
        #
        ########
        _logger.error("datetime.now() ++ " + str(datetime.now()))
        orders = self.env['meal.order'].search([('state', 'in', ('confirmed', 'in_process')),
                              '|', '&', ('order_type', '=', 'external'), ('order_date', '>', datetime.now().date()),
                              '&', ('order_type', '=', 'internal'), ('table_number', '=', 0)],
                                               limit=2,
                                               order="name"
                                               )
        # orders = self.env['meal.order'].search_count([('state', 'in', ('confirmed', 'in_process')),
        #                                         '|', '&', ('order_type', '=', 'external'),
        #                                         ('order_date', '>', datetime.now().date()),
        #                                         '&', ('order_type', '=', 'internal'), ('table_number', '=', 0)],
        #
        #                                        )

        # order_len = len(orders)

        #select name, order_type, customer_id form meal_order;
        #######
        # orders = orders.read(['name', 'order_type', 'customer_id'])

        #######
        # select name, type, customer where ... group_by name
        # orders = self.read_group([('state', 'in', ('confirmed', 'in_process')),
        #    '|', '&', ('order_type', '=', 'external'), ('expected_date', '<', datetime.now()),
        #  '&', ('order_type', '=', 'internal'), ('table_number', '=', 0)],
        #     ['name', 'order_type', 'customer_id'],
        #   ['order_type', 'customer_id'],
        #    lazy=True)
        # orders[0].unlink()
        #  offset=1
        #  limit=1
        # order = 'order_date ASC'
        # orderby = 'order_date',
        # count = True
        #######
        # orders[0].copy({'name':str(orders[0].id)})
        # raise ValidationError(str(orders))

        # Environment.ref(external id) --> get object
        # raise ValidationError(str(self.env.ref('base.res_partner_address_15').name))


        # Environment.user
        # raise ValidationError(str(self.env.user))

        # Environment.tz,lang
        # _logger.error("Time Zone " + str(self.env.tz))
        # raise ValidationError(str(self.env.lang))

        # Model.with_context
        orders[0].with_context({'cancelled_value':True}).action_cancelled()
        #
        # Model.with_user
        #
        # Model.sudo








