from django.db import models
from .Project import Project # Import the Project model
# from .Alert import Alert   # Alert has FK to Outage, so direct import here is not strictly needed for the FK definition but good for reverse relation

class Outage(models.Model):
    outage_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE, # Assuming deleting a project cascades to its outages
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
        app_label = 'app'

    def __str__(self):
        return f"Outage {self.outage_id} - Resolved: {self.resolved}"