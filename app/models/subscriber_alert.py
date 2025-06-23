
from django.db import models
from .user import User
from .alert_type import AlertType
class SubscriberAlert(models.Model):
    """Django equivalent of the Laravel SubscriberAlert model."""
    subscriber_alert_id = models.AutoField(primary_key=True)
    message = models.TextField()
    active = models.BooleanField(default=True)
    
    # Relationships
    subscriber = models.ForeignKey('Subscriber', on_delete=models.CASCADE, related_name='alerts', db_column='subscriber_id')
    alert_type = models.ForeignKey(AlertType, on_delete=models.PROTECT, db_column='alert_type_id')
    activated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='activated_subscriber_alerts',
        db_column='activated_by'
    )
    deactivated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='deactivated_subscriber_alerts',
        db_column='deactivated_by'
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='updated_subscriber_alerts',
        db_column='updated_by'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "subscriber_alerts"
        ordering = ['-created_at']