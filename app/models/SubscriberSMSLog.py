from django.db import models


class SubscriberSMSLog(models.Model):
    """Django equivalent of the Laravel SubscriberSMSLog model."""
    subscriber_sms_log_id = models.AutoField(primary_key=True)
    sent_to = models.CharField(max_length=20)
    success = models.BooleanField()

    # Relationships
    item = models.ForeignKey('SMSLogItem', on_delete=models.CASCADE, db_column='sms_log_item_id')
    subscriber = models.ForeignKey('Subscriber', on_delete=models.CASCADE, db_column='subscriber_id')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subscriber_sms_log'
        ordering = ['-created_at']