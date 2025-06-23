from django.db import models
from .time_stamped_model_mixin import TimeStampedModelMixin

class BulkMessageType(TimeStampedModelMixin, models.Model):
    bulk_message_type_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'bulk_message_type'
        app_label = 'app' 

    def __str__(self):
        return self.description 