from django.db import models

class TicketEntryActionType(models.Model):
    ticket_entry_action_type_id = models.AutoField(primary_key=True)
    # Assuming this type has a descriptive field, like 'name' or 'description'.
    name = models.CharField(max_length=255, unique=True) # Common for type tables
    # Laravel models often implicitly handle created_at/updated_at. Adding them for completeness.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ticket_entry_action_types'
        app_label = 'app'

    def __str__(self):
        return self.name