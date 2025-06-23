from django.db import models
from .us_state import UsState # Import the UsState model
from .user import User # Import the User model
from .time_stamped_model_mixin import TimeStampedModelMixin

class InterestFormLog(TimeStampedModelMixin, models.Model):
    """Django equivalent of the Laravel InterestFormLog model."""
    interest_form_log_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    notes = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    state = models.ForeignKey(UsState, on_delete=models.PROTECT, db_column='state_id')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, db_column='updated_by_id')


    class Meta:
        db_table = "interest_form_log"
        ordering = ['-created_at']

    def __str__(self):
        return f"Interest form from {self.name} on {self.created_at.date()}"