from django.db import models

class TicketCategory(models.Model):
    """Django equivalent of the Laravel TicketCategory model."""
    ticket_category_id = models.AutoField(primary_key=True)
    description = models.TextField()

    class Meta:
        db_table = 'ticket_category'

    def __str__(self):
        return self.description