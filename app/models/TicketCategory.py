from django.db import models

class TicketCategory(models.Model):
    ticket_category_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, unique=True) # Assuming a unique descriptive name for the category
    # Laravel models often implicitly handle created_at/updated_at. Adding them for completeness.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ticket_category' # Note: Table name is singular as per Laravel model
        app_label = 'app'

    def __str__(self):
        return self.description