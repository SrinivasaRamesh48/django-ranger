from django.db import models
from .time_stamped_model_mixin import TimeStampedModelMixin
class StatementItemType(TimeStampedModelMixin, models.Model):
    """Django equivalent of the Laravel StatementItemType model."""
    statement_item_type_id = models.AutoField(primary_key=True)
    description = models.TextField()

    class Meta:
        db_table = 'statement_item_types'

    def __str__(self):
        return self.description[:50]