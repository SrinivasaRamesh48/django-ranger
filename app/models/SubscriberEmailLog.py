
from django.db import models

class SubscriberEmailLog(models.Model):
    """Django equivalent of the Laravel SubscriberEmailLog model."""
    subscriber_email_log_id = models.AutoField(primary_key=True)
    sent_to = models.EmailField()
    success = models.BooleanField()

    # Relationships
    item = models.ForeignKey('EmailLogItem', on_delete=models.CASCADE, db_column='email_log_item_id')
    subscriber = models.ForeignKey('Subscriber', on_delete=models.CASCADE, db_column='subscriber_id')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subscriber_email_log'
        ordering = ['-created_at']