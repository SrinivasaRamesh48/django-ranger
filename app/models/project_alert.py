from django.db import models
from app.models.time_stamped_model_mixin import TimeStampedModelMixin
class ProjectAlert(TimeStampedModelMixin, models.Model):
    """Django equivalent of the Laravel ProjectAlert model."""
    project_alert_id = models.AutoField(primary_key=True)
    message = models.TextField()
    active = models.BooleanField(default=True)
    
    # Relationships
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name='alerts', db_column='project_id')
    alert_type = models.ForeignKey("AlertType", on_delete=models.PROTECT, db_column='alert_type_id')
    activated_by = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True, related_name='activated_project_alerts')
    deactivated_by = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True, related_name='deactivated_project_alerts')
    updated_by = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_project_alerts')

    class Meta:
        db_table = "project_alerts"
        ordering = ['-created_at']