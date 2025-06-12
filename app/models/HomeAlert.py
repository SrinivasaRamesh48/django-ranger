from django.db import models
from django.contrib.auth import get_user_model # Use get_user_model for User

from .AlertType import AlertType 
from .Home import Home            

User = get_user_model() 
class HomeAlert(models.Model):
    home_alert_id = models.AutoField(primary_key=True)
    alert_type = models.ForeignKey(
        AlertType,
        on_delete=models.CASCADE, 
        db_column='alert_type_id',
        related_name='home_alerts'
    )
    home = models.ForeignKey(
        Home,
        on_delete=models.CASCADE, # If the home is deleted, its alerts go too
        db_column='home_id',
        related_name='home_alerts'
    )
    message = models.TextField()
    active = models.BooleanField(default=True) # Assuming active is a boolean 0/1
    activated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='activated_by',
        related_name='home_alerts_activated'
    )
    deactivated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='deactivated_by',
        related_name='home_alerts_deactivated'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='updated_by',
        related_name='home_alerts_updated'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'home_alerts'
        app_label = 'app'

    def __str__(self):
        return f"Home Alert {self.home_alert_id} for Home {self.home_id} - {self.message[:50]}..."