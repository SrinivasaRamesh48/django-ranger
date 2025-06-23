from django.db import models
from app.models.time_stamped_model_mixin import TimeStampedModelMixin

class SubscriberSMSLog(TimeStampedModelMixin, models.Model):
    """Django equivalent of the Laravel SubscriberSMSLog model."""
    subscriber_sms_log_id = models.AutoField(primary_key=True)
    sent_to = models.CharField(max_length=20)
    success = models.BooleanField()

    # Relationships
    item = models.ForeignKey('SMSLogItem', on_delete=models.CASCADE, db_column='sms_log_item_id')
    subscriber = models.ForeignKey('Subscriber', on_delete=models.CASCADE, db_column='subscriber_id')



    class Meta:
        db_table = 'subscriber_sms_log'
        ordering = ['-created_at']