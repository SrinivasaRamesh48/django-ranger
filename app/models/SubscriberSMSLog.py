from django.db import models
from .Subscriber import Subscriber  # Import the Subscriber model
from .SMSLogItem import SMSLogItem # Import the SMSLogItem model

class SubscriberSMSLog(models.Model):
    subscriber_sms_log_id = models.AutoField(primary_key=True)
    subscriber = models.ForeignKey(
        Subscriber,
        on_delete=models.CASCADE, # If subscriber is deleted, log entries are removed
        db_column='subscriber_id',
        related_name='sms_logs'
    )
    sent_to = models.CharField(max_length=20) # Phone number it was sent to, e.g., E.164 format
    sms_log_item = models.ForeignKey(
        SMSLogItem,
        on_delete=models.SET_NULL, # Assuming log might remain even if the SMS item is deleted
        null=True, blank=True,
        db_column='sms_log_item_id',
        related_name='subscriber_sms_logs'
    )
    success = models.BooleanField(default=False)
    # Laravel models often implicitly handle created_at/updated_at even if not in fillable.
    # If your table has these, define them:
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subscriber_sms_log' # Note: Table name is singular as per Laravel model
        app_label = 'app'

    def __str__(self):
        return f"SMS Log {self.subscriber_sms_log_id} - To: {self.sent_to}"