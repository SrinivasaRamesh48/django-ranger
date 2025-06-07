from django.db import models
from .Outage import Outage          # Import the Outage model
from .BulkMessageType import BulkMessageType # Import the BulkMessageType model

class SMSLogItem(models.Model):
    sms_log_item_id = models.AutoField(primary_key=True)
    body = models.TextField() # Content of the SMS
    outage = models.ForeignKey(
        Outage,
        on_delete=models.SET_NULL, # Assuming SMS logs might remain even if outage is deleted
        null=True, blank=True,
        db_column='outage_id',
        related_name='sms_log_items'
    )
    bulk_message_type = models.ForeignKey(
        BulkMessageType,
        on_delete=models.SET_NULL, # Assuming SMS logs might remain even if message type is deleted
        null=True, blank=True,
        db_column='bulk_message_type_id',
        related_name='sms_log_items'
    )
    # Laravel models often implicitly handle created_at/updated_at even if not in fillable.
    # If your table has these, define them:
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sms_log_items'
        app_label = 'app'

    def __str__(self):
        return f"SMS Log Item {self.sms_log_item_id} - {self.body[:50]}..."