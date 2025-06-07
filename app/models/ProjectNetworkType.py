from django.db import models

class ProjectNetworkType(models.Model):
    project_network_type_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, unique=True) # Assuming a unique descriptive name for the type
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project_network_type' # Note: Table name is singular as per Laravel model
        app_label = 'app'

    def __str__(self):
        return self.description