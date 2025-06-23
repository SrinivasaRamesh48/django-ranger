from django.db import models
from app.models.time_stamped_model_mixin import TimeStampedModelMixin
class ServiceChangeScheduleType(TimeStampedModelMixin, models.Model):
    service_change_schedule_type_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, unique=True) # Assuming a unique descriptive name for the type

    class Meta:
        db_table = 'service_change_schedule_type' # Note: Table name is singular as per Laravel model
        app_label = 'app'

    def __str__(self):
        return self.description