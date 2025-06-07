from django.db import models
from django.contrib.auth import get_user_model

# Assuming you have models for Ticket and User
from .Ticket import Ticket
User = get_user_model()


class TicketEntry(models.Model):
    ticket_entry_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name='entries', db_column='ticket_id')
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, db_column='user_id', related_name='ticket_entries')
    description = models.TextField()
    notes_private = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    submitted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ticket_entry'  # Use singular name to match Laravel
        app_label = 'app'

    def __str__(self):
        return f"Ticket Entry {self.ticket_entry_id} for Ticket {self.ticket_id}"