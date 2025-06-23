from django.db import models
from .outage import Outage          # Import the Outage model
from .bulk_message_type import BulkMessageType # Import the BulkMessageType model
from .time_stamped_model_mixin import TimeStampedModelMixin  # Import the mixin for timestamp fields
class SMSLogItem(TimeStampedModelMixin, models.Model):
    """Django equivalent of the Laravel SMSLogItem model."""
    sms_log_item_id = models.AutoField(primary_key=True)
    body = models.TextField()
    outage = models.ForeignKey('Outage', on_delete=models.SET_NULL, null=True, blank=True, db_column='outage_id')
    bulk_message_type = models.ForeignKey('BulkMessageType', on_delete=models.SET_NULL, null=True, blank=True, db_column='bulk_message_type_id')


    class Meta:
        db_table = "sms_log_items"
    