from django.db import models
from .StatementItemType import StatementItemType # Import the StatementItemType model

class StatementItemDescription(models.Model):
    """Django equivalent of the Laravel StatementItemDescription model."""
    statement_item_description_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    
    # Relationship
    type = models.ForeignKey(StatementItemType, on_delete=models.PROTECT, db_column='statement_item_type_id')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'statement_item_descriptions'

    def __str__(self):
        return self.description