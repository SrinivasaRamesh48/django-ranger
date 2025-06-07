from django.db import models
from django.contrib.auth import get_user_model # Use get_user_model for User

from .AlertType import AlertType  # Import the AlertType model
from .Project import Project      # Import the Project model

User = get_user_model() # Get the currently active user model

class ProjectAlert(models.Model):
    project_alert_id = models.AutoField(primary_key=True)
    alert_type = models.ForeignKey(
        AlertType,
        on_delete=models.CASCADE, # If the alert type is deleted, these alerts go too
        db_column='alert_type_id',
        related_name='project_alerts'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE, # If the project is deleted, its alerts go too
        db_column='project_id',
        related_name='project_alerts'
    )
    message = models.TextField()
    active = models.BooleanField(default=True) # Assuming active is a boolean 0/1
    activated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='activated_by',
        related_name='project_alerts_activated'
    )
    deactivated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='deactivated_by',
        related_name='project_alerts_deactivated'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='updated_by',
        related_name='project_alerts_updated'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project_alerts'
        app_label = 'app'

    def __str__(self):
        return f"Project Alert {self.project_alert_id} for Project {self.project_id} - {self.message[:50]}..."