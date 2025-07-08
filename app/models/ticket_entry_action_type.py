from django.db import models

class TicketEntryActionType(models.Model):
    ticket_entry_action_type_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    description_past_tense = models.CharField(max_length=255, blank=True, null=True)
    identifier = models.CharField(max_length=50, unique=True)
    display = models.ImageField(default=0)
    icon = models.CharField(max_length=50, blank=True, null=True)
    display_message = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'ticket_entry_action_types'

    def __str__(self):
        return self.description