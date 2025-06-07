from django.db import models
from django.contrib.auth import get_user_model # Use get_user_model for User

from .AlertType import AlertType
from .Subscriber import Subscriber

User = get_user_model()

class SubscriberAlert(models.Model):
    subscriber_alert_id = models.AutoField(primary_key=True)
    alert_type = models.ForeignKey(AlertType, on_delete=models.CASCADE, db_column='alert_type_id', related_name='subscriber_alerts')
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, db_column='subscriber_id', related_name='subscriber_alerts')
    message = models.TextField()
    active = models.BooleanField(default=True)
    activated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='activated_by', related_name='subscriber_alerts_activated')
    deactivated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deactivated_by', related_name='subscriber_alerts_deactivated')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', related_name='subscriber_alerts_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subscriber_alerts'
        app_label = 'app'

    def __str__(self):
        return f"Subscriber Alert {self.subscriber_alert_id} for Subscriber {self.subscriber_id} - {self.message[:50]}..."