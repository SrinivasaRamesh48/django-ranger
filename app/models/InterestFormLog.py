from django.db import models
from django.contrib.auth import get_user_model # Use get_user_model for User

from .UsState import UsState # Import the UsState model

User = get_user_model() # Get the currently active user model

class InterestFormLog(models.Model):
    interest_form_log_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.ForeignKey(
        UsState,
        on_delete=models.SET_NULL, # Assuming log might remain if state is deleted
        null=True, blank=True,
        db_column='state_id',
        related_name='interest_form_logs'
    )
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True) # Assuming phone is a string
    message = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='updated_by_id',
        related_name='interest_form_logs_updated'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True) # Can be IPv4 or IPv6
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'interest_form_log' 
        app_label = 'app'

    def __str__(self):
        return f"Interest Form Log {self.interest_form_log_id} - {self.name}"