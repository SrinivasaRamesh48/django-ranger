from django.db import models

class TicketStatus(models.Model):
    ticket_status_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'ticket_status' # Note: Table name is singular as per Laravel model
        app_label = 'app'

    def __str__(self):
        return self.description