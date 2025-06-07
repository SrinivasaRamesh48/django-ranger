from django.db import models
from django.contrib.auth import get_user_model

# Assuming you have models for TicketCategory and TicketStatus
from .TicketCategory import TicketCategory
from .TicketStatus import TicketStatus
from .Subscriber import Subscriber  # Ensure Subscriber model is defined

User = get_user_model()


class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    subscriber = models.ForeignKey(
        Subscriber, on_delete=models.CASCADE, related_name='tickets', db_column='subscriber_id'
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets', db_column='user_id'
    )
    ticket_category = models.ForeignKey(
        TicketCategory,
        on_delete=models.SET_DEFAULT,
        default=2,  # Matches Laravel's default value.  If TicketCategory is not defined, use an IntegerField here.
        db_column='ticket_category_id',
        related_name='tickets'
    )
    ticket_status = models.ForeignKey(
        'TicketStatus', # Or TicketStatus if it's already defined
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='ticket_status_id',
        related_name='tickets'
    )
    opened_on = models.DateTimeField()
    reopened_on = models.DateTimeField(null=True, blank=True)
    closed_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'tickets'
        app_label = 'app'

    def __str__(self):
        return f"Ticket {self.ticket_id}"