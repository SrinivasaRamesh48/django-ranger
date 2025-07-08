from django.db import models
from app.models.time_stamped_model_mixin import TimeStampedModelMixin


class NodeType(TimeStampedModelMixin, models.Model):
    node_type_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, unique=True, blank=False)
    max_ports = models.IntegerField(null=True, blank=True)
    subscriber_switch = models.IntegerField(default=0, blank=False)
    speed = models.IntegerField(null=True, blank=True)
   
    class Meta:
        db_table = 'node_types'
        app_label = 'app'


    def __str__(self):
        return self.description