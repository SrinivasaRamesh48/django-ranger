from django.db import models
from .Outage import Outage
from .Project import Project  

class DowntimeEvent(models.Model):
    """Django equivalent of the Laravel DowntimeEvent model."""
    downtime_event_id = models.AutoField(primary_key=True)
    outage = models.ForeignKey(Outage, on_delete=models.CASCADE, db_column='outage_id')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, db_column='project_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "downtime_event"
        ordering = ['-created_at']
    def __str__(self):
        return f"Downtime Event for Outage {self.outage_id}"