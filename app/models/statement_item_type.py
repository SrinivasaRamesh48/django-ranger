from django.db import models
from .time_stamped_model_mixin import TimeStampedModelMixin


class StatementItemType(TimeStampedModelMixin, models.Model):
    statement_item_type_id = models.AutoField(primary_key=True)
    description = models.TextField()

    class Meta:
        db_table = 'statement_item_types'

    def __str__(self):
        return self.description[:50]