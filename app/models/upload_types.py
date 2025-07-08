from django.db import models

class UploadType(models.Model):
    upload_type_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, unique=True) 

    class Meta:
        db_table = 'upload_types' 
        app_label = 'app'

    def __str__(self):
        return self.description