from django.db import models
from app.models.time_stamped_model_mixin import TimeStampedModelMixin
class ProjectNetworkType(TimeStampedModelMixin, models.Model):
    project_network_type_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, unique=True)
    class Meta:
        db_table = 'project_network_type' # Note: Table name is singular as per Laravel model
        app_label = 'app'

    def __str__(self):
        return self.description