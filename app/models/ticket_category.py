from django.db import models

class TicketCategory(models.Model):
    ticket_category_id = models.AutoField(primary_key=True)
    description = models.TextField()
    account_portal_visible = models.IntegerField(default=0)
    class Meta:
        db_table = 'ticket_category'

    def __str__(self):
        return self.description