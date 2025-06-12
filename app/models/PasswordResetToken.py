from django.db import models

class PasswordResetToken(models.Model):
    password_reset_token_id = models.AutoField(primary_key=True)
    subscriber = models.ForeignKey(
        'Subscriber',  
        on_delete=models.CASCADE,  
        db_column='subscriber_id',
        related_name='password_reset_tokens'
    )
    token = models.CharField(max_length=255)
    expires = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'password_reset_tokens'
        app_label = 'app'

    def __str__(self):
        return f"Password Reset Token for Subscriber {self.subscriber_id}"