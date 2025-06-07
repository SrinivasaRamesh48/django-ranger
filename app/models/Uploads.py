from django.db import models

# Import all related models
from .Project import Project   # Assuming Project model exists
from .Circuit import Circuit   # Assuming Circuit model exists
from .Home import Home         # Assuming Home model exists
from .Subscriber import Subscriber # Assuming Subscriber model exists
from .UploadTypes import UploadType 

class Uploads(models.Model):
    upload_id = models.AutoField(primary_key=True)
    # Foreign Keys - assuming an upload can be related to one of these (or none initially)
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL, # Upload might remain if project is deleted
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
        Home,
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
    # Foreign Key to UploadType (Laravel used UploadTypes, singularized for Django)
    upload_type = models.ForeignKey(
        UploadType,
        on_delete=models.CASCADE, # If the type is deleted, these uploads are too
        db_column='upload_type_id',
        related_name='uploads'
    )
    name = models.CharField(max_length=255) # Name of the file/upload
    # FileField handles file storage and paths. Requires MEDIA_ROOT/MEDIA_URL in settings.
    path = models.FileField(upload_to='uploads/') # 'uploads/' is a subdirectory within MEDIA_ROOT
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'uploads'
        app_label = 'app'

    def __str__(self):
        return f"Upload {self.upload_id} - {self.name}"