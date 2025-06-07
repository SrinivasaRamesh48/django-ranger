from django.db import models

class NodeType(models.Model):
    node_type_id = models.AutoField(primary_key=True)
    # Assuming this type has a descriptive field, like 'name' or 'description'
    name = models.CharField(max_length=255, unique=True) # Common for type tables
    # Add any other fields that might be in your 'node_types' table

    class Meta:
        db_table = 'node_types'
        app_label = 'app'

    def __str__(self):
        return self.name