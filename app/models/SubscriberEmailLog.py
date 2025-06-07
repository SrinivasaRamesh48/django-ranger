from django.db import models
from .Subscriber import Subscriber  # Import the Subscriber model
from .EmailLogItem import EmailLogItem # Import the EmailLogItem model

class SubscriberEmailLog(models.Model):
    subscriber_email_log_id = models.AutoField(primary_key=True)
    subscriber = models.ForeignKey(
        Subscriber,
        on_delete=models.CASCADE, # If subscriber is deleted, log entries are removed
        db_column='subscriber_id',
        related_name='email_logs'
    )
    sent_to = models.EmailField() # Email address it was sent to
    email_log_item = models.ForeignKey(
        EmailLogItem,
        on_delete=models.SET_NULL, # Assuming log might remain even if the email item is deleted
        null=True, blank=True,
        db_column='email_log_item_id',
        related_name='subscriber_email_logs'
    )
    success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subscriber_email_log' # Note: Table name is singular as per Laravel model
        app_label = 'app'

    def __str__(self):
        return f"Email Log {self.subscriber_email_log_id} - To: {self.sent_to}"