from django.db import models
from .alert_type import AlertType   
from .user import User  

class Alert(models.Model):
    alert_id = models.AutoField(primary_key=True)
    alert_type = models.ForeignKey(
        AlertType,
        on_delete=models.PROTECT, 
        db_column='alert_type_id',
    )
    message = models.TextField(help_text="The content of the alert message.")
    active = models.BooleanField(default=True, help_text="Indicates if the alert is currently active.")
    activated_by = models.ForeignKey(
        User,
        related_name='activated_alerts',
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        db_column='activated_by'
    )
    deactivated_by = models.ForeignKey(
        User,
        related_name='deactivated_alerts',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='deactivated_by'
    )
    updated_by = models.ForeignKey(
        User,
        related_name='updated_alerts',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='updated_by'
    )

    outage = models.ForeignKey(
        'Outage',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='outage_id',
        related_name='alert'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "alerts"

    def __str__(self):
        return f"Alert ({self.alert_type.name}): {self.message[:50]}..."