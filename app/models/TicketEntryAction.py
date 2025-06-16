from django.db import models
from .TicketEntryActionType import TicketEntryActionType # Import the TicketEntryActionType model
class TicketEntryAction(models.Model):
    """Django equivalent of the Laravel TicketEntryAction model."""
    ticket_entry_action_id = models.AutoField(primary_key=True)
    
    # Relationships
    ticket_entry = models.ForeignKey('TicketEntry', on_delete=models.CASCADE, related_name='actions', db_column='ticket_entry_id')
    type = models.ForeignKey(TicketEntryActionType, on_delete=models.CASCADE, db_column='ticket_entry_action_type_id')

    class Meta:
        db_table = 'ticket_entry_action'