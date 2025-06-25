from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    max_table_number = fields.Integer(string="Max Table Number")
    
    def set_values(self):
        res = super().set_values()
        self.env['ir.config_parameter'].set_param('tech_order.max_table_number',
                                                  self.max_table_number)
        return res
    
    def get_values(self):
        res = super().get_values()
        value = self.env['ir.config_parameter'].sudo().get_param('tech_order.max_table_number')
        res.update(max_table_number=int(value))
        return res


