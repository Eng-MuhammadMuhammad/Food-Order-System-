from odoo import models, fields

class MealIngredient(models.Model):
    _name = 'meal.ingredient'
    _description = "Meal Ingredient"

    name = fields.Char("Name", required=True)
    product_id = fields.Many2one('product.product', string="product")
    meal_id = fields.Many2one('order.meal', string="Meal", copy=False)
    quantity = fields.Float("Quantity")