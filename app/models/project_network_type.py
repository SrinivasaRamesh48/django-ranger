from django.db import models


class ProjectNetworkType( models.Model):
    project_network_type_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, unique=True)
    class Meta:
        db_table = 'project_network_type' 
        app_label = 'app'

    def __str__(self):
        return self.description