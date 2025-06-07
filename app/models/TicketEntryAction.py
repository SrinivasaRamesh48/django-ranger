from django.db import models
from .TicketEntry import TicketEntry           # Import the TicketEntry model
from .TicketEntryActionType import TicketEntryActionType # Import the TicketEntryActionType model

class TicketEntryAction(models.Model):
    ticket_entry_action_id = models.AutoField(primary_key=True)
    ticket_entry = models.ForeignKey(
        TicketEntry,
        on_delete=models.CASCADE, # If ticket entry is deleted, actions are too
        db_column='ticket_entry_id',
        related_name='actions'
    )
    ticket_entry_action_type = models.ForeignKey(
        TicketEntryActionType,
        on_delete=models.CASCADE, # If action type is deleted, these actions are too
        db_column='ticket_entry_action_type_id',
        related_name='ticket_entry_actions'
    )
    # Laravel models often implicitly handle created_at/updated_at. Adding them for completeness.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ticket_entry_action' # Note: Table name is singular as per Laravel model
        app_label = 'app'

    def __str__(self):
        return f"Ticket Entry Action {self.ticket_entry_action_id} (Type: {self.ticket_entry_action_type_id})"