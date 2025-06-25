from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta

import logging
_logger = logging.getLogger(__name__)

class FeedbackReason(models.TransientModel):
    _name="feedback.reason"
    _description = "Feedback Reason"

    reason = fields.Char('Reason', required=True)

    def add_reason(self):
        # context = {'active_id':self.id}
        feedback_id = self.env.context.get('active_id')
        _logger.error("ACTIVE ID +++ " + str(feedback_id))
        feedback = self.env['customer.feedback'].browse(feedback_id)
        # Browse --> in (id or list of ids), Out(object, list of objects)
        _logger.error("feedback  +++ " + str(feedback))
        # feedback.state = 'rejected'
        # feedback.reason = self.reason
        feedback.update({
            'state': 'rejected',
            'reason': self.reason
        })
        # update OR write




