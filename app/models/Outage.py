from django.db import models

from app.models.alert import Alert
from .project import Project
from .outage_homes_effected import OutageHomesEffected  

class Outage(models.Model):
    outage_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        db_column='project_id',
        related_name='outages'
    )
    resolved = models.BooleanField(default=False)
    email_notices_sent = models.BooleanField(default=False)
    phone_notices_sent = models.BooleanField(default=False)
    phone_message_updated = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'outages'
        ordering = ['-created_at']

    def __str__(self):
        return f"Outage {self.outage_id}"
