from django.db import models

from .project import Project 
from .circuit import Circuit 
 
from .subscriber import Subscriber
from .upload_types import UploadType 
from .time_stamped_model_mixin import TimeStampedModelMixin

class Uploads(TimeStampedModelMixin, models.Model):
    upload_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='project_id',
        related_name='uploads'
    )
    circuit = models.ForeignKey(
        Circuit,
        on_delete=models.SET_NULL, # Upload might remain if circuit is deleted
        null=True, blank=True,
        db_column='circuit_id',
        related_name='uploads'
    )
    home = models.ForeignKey(
        'Home',
        on_delete=models.SET_NULL, # Upload might remain if home is deleted
        null=True, blank=True,
        db_column='home_id',
        related_name='uploads'
    )
    subscriber = models.ForeignKey(
        Subscriber,
        on_delete=models.SET_NULL, # Upload might remain if subscriber is deleted
        null=True, blank=True,
        db_column='subscriber_id',
        related_name='uploads'
    )

    upload_type = models.ForeignKey(
        UploadType,
        on_delete=models.CASCADE, 
        db_column='upload_type_id',
        related_name='uploads'
    )
    name = models.CharField(max_length=255) 
    path = models.FileField(upload_to='uploads/') # 

    class Meta:
        db_table = 'uploads'

    def __str__(self):
        return f"Upload {self.upload_id} - {self.name}"