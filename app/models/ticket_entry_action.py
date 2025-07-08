from django.db import models
from .ticket_entry_action_type import TicketEntryActionType
from .time_stamped_model_mixin import TimeStampedModelMixin

class TicketEntryAction(TimeStampedModelMixin, models.Model):
    ticket_entry_action_id = models.AutoField(primary_key=True)
    
    # Relationships
    ticket_entry = models.ForeignKey('TicketEntry', on_delete=models.CASCADE, related_name='actions', db_column='ticket_entry_id')
    type = models.ForeignKey(TicketEntryActionType, on_delete=models.CASCADE, db_column='ticket_entry_action_type_id')

    class Meta:
        db_table = 'ticket_entry_action'