from django.db import models
from app.models.project import Project


class NodeFrame(models.Model):
    """Django equivalent of the Laravel NodeFrame model."""
    node_frame_id = models.AutoField(primary_key=True)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'node_frames'
    def __str__(self):
        return self.description[:50]