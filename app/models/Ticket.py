from django.db import models
from .user import User
from .ticket_category import TicketCategory
from .time_stamped_model_mixin import TimeStampedModelMixin
class Ticket(TimeStampedModelMixin, models.Model):
    ticket_id = models.AutoField(primary_key=True)
    opened_on = models.DateTimeField(auto_now_add=True)
    reopened_on = models.DateTimeField(null=True, blank=True)
    closed_on = models.DateTimeField(null=True, blank=True)

    # Relationships
    subscriber = models.ForeignKey('Subscriber', on_delete=models.CASCADE, related_name='tickets', db_column='subscriber_id')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='user_id')
    ticket_category = models.ForeignKey(TicketCategory, on_delete=models.PROTECT, db_column='ticket_category_id', default=2)
    ticket_status = models.ForeignKey('TicketStatus', on_delete=models.PROTECT, db_column='ticket_status_id')
    
    class Meta:
        db_table = "tickets"
        ordering = ['-opened_on']

    def __str__(self):
        return f"Ticket #{self.ticket_id} for Subscriber {self.subscriber_id}"
