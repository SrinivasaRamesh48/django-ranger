from django.db import models
from .Outage import Outage
from .Project import Project  

class DowntimeEvent(models.Model):
    downtime_event_id = models.AutoField(primary_key=True)
    outage = models.ForeignKey(
        Outage,
        on_delete=models.CASCADE,
        db_column='outage_id',
        related_name='downtime_events'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE, 
        db_column='project_id',
        related_name='downtime_events'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'downtime_event' 
        app_label = 'app'

    def __str__(self):
        return f"Downtime Event {self.downtime_event_id} for Project {self.project_id}"