from django.db import models

class PasswordResetToken(models.Model):
    """Django equivalent of the Laravel PasswordResetToken model."""
    password_reset_token_id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=255)
    expires = models.DateTimeField()
    subscriber = models.ForeignKey('Subscriber', on_delete=models.CASCADE, db_column='subscriber_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'password_reset_tokens'