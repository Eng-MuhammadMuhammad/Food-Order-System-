from odoo import models, fields,api,_
from odoo.exceptions import ValidationError


class MealCategory(models.Model):
    _name='order.meal.category'

    name = fields.Char("Name", required=True) #, copy=False

class Meal(models.Model):
    _name='order.meal'

    name = fields.Char("Name", required=True)
    price = fields.Float("Price", readonly=False)
    category_id = fields.Many2one('order.meal.category', string="Category", ondelete="restrict")# cascade
    ingredient_ids = fields.One2many('meal.ingredient', 'meal_id', string="Ingredient")
    feedback_ids = fields.One2many('customer.feedback','meal_id', string="FeedBacks")

    @api.onchange('price')
    def check_price(self):
        if self.price < 0:
            raise ValidationError(_("Price must not be 0"))

    def action_view_feedback(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Feedback',
            'view_mode': 'list',
            'res_model': 'customer.feedback',
            'target': 'current',
            'domain': [('id', 'in', self.feedback_ids.ids)],
            'context': {'default_meal_id': self.id}

        }
        # self.feedback_ids.ids ==> [1,5,7]
        # 'context': {'create': True, 'default_meal_id': self.id}










