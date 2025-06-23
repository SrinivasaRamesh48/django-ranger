from django.db import models

class TicketEntryActionType(models.Model):
    ticket_entry_action_type_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=255, unique=True) 

    class Meta:
        db_table = 'ticket_entry_action_types'

    def __str__(self):
        return self.name