from django.db import models
from .StatementItemType import StatementItemType # Import the StatementItemType model

class StatementItemDescription(models.Model):
    statement_item_description_id = models.AutoField(primary_key=True)
    description = models.TextField() # Assuming description can be a longer text
    statement_item_type = models.ForeignKey(
        StatementItemType,
        on_delete=models.CASCADE, # Assuming deleting a type cascades to its descriptions
        db_column='statement_item_type_id',
        related_name='statement_item_descriptions'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'statement_item_descriptions'
        app_label = 'app'

    def __str__(self):
        return self.description[:50] # Return first 50 chars of description