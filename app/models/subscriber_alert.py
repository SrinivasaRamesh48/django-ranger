
from django.db import models
from .user import User
from .alert_type import AlertType
from .time_stamped_model_mixin import TimeStampedModelMixin

class SubscriberAlert(TimeStampedModelMixin, models.Model):
    subscriber_alert_id = models.AutoField(primary_key=True)
    message = models.TextField()
    active = models.IntegerField(default=1)
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
    
    
    class Meta:
        db_table = "subscriber_alerts"
        ordering = ['-created_at']