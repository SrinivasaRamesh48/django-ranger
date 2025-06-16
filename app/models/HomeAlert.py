from django.db import models
from .User import User
from .AlertType import AlertType 
from .Home import Home            
from .TimeStampedModelMixin import TimeStampedModelMixin

class HomeAlert(TimeStampedModelMixin, models.Model):
    home_alert_id = models.AutoField(primary_key=True)
    home = models.ForeignKey('Home', on_delete=models.CASCADE, related_name='alerts', db_column='home_id')
    alert_type = models.ForeignKey(AlertType, on_delete=models.PROTECT, db_column='alert_type_id')
    message = models.TextField()
    active = models.BooleanField(default=True)
    activated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activated_home_alerts', db_column='activated_by')
    deactivated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='deactivated_home_alerts', db_column='deactivated_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_home_alerts', db_column='updated_by')

    class Meta:
        db_table = 'home_alerts'
        ordering = ['-created_at']
    def __str__(self):
        return f"Alert for {self.home.address}: {self.message[:30]}"