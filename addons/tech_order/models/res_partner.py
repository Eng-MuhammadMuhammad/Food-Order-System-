from odoo import models, fields,api,_
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class RESPartner(models.Model):
    _inherit = "res.partner"
    # _name="res.partner"

    feedbacks_ids = fields.One2many('customer.feedback', 'customer_id',
                                    string="FeedBacks", readonly=1)



