from django.db import models
from .time_stamped_model_mixin import TimeStampedModelMixin



class NodeClass(TimeStampedModelMixin, models.Model):
    node_class_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, unique=True) 
    class Meta:
        db_table = 'node_class' # Note: Table name is singular as per Laravel model
        app_label = 'app'

    def __str__(self):
        return self.description