from django.db import models

class UploadType(models.Model):
    upload_type_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, unique=True) # Assuming a unique descriptive name for the type
    # Laravel models often implicitly handle created_at/updated_at. Adding them for completeness.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'upload_types' # Matches your Laravel protected $table
        app_label = 'app'

    def __str__(self):
        return self.description