from django.db import models
from .statement_item_type import StatementItemType # Import the StatementItemType model
from .time_stamped_model_mixin import TimeStampedModelMixin  # Import the mixin for timestamp fields
class StatementItemDescription(TimeStampedModelMixin, models.Model):
    """Django equivalent of the Laravel StatementItemDescription model."""
    statement_item_description_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    
    # Relationship
    type = models.ForeignKey(StatementItemType, on_delete=models.PROTECT, db_column='statement_item_type_id')

    
    class Meta:
        db_table = 'statement_item_descriptions'

    def __str__(self):
        return self.description