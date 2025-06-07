from django.db import models
from .Project import Project # Import the Project model

class NodeFrame(models.Model):
    node_frame_id = models.AutoField(primary_key=True) # Assuming this is the correct PK column name
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE, # Assuming deleting a project cascades to its node frames
        db_column='project_id',
        related_name='node_frames'
    )
    description = models.TextField(blank=True, null=True) # Using TextField for description, can be CharField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'node_frames'
        app_label = 'app'

    def __str__(self):
        return self.description or f"Node Frame {self.node_frame_id}"