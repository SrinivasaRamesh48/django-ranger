from django.db import models
from .time_stamped_model_mixin import TimeStampedModelMixin

class PasswordResetToken(TimeStampedModelMixin, models.Model):
    """Django equivalent of the Laravel PasswordResetToken model."""
    password_reset_token_id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=255)
    expires = models.DateTimeField()
    subscriber = models.ForeignKey('Subscriber', on_delete=models.CASCADE, db_column='subscriber_id')
    class Meta:
        db_table = 'password_reset_tokens'