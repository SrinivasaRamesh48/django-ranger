from django.db import models
from .Outage import Outage          # Import the Outage model
from .BulkMessageType import BulkMessageType # Import the BulkMessageType model

class SMSLogItem(models.Model):
    """Django equivalent of the Laravel SMSLogItem model."""
    sms_log_item_id = models.AutoField(primary_key=True)
    body = models.TextField()

   
    outage = models.ForeignKey('Outage', on_delete=models.SET_NULL, null=True, blank=True, db_column='outage_id')
    bulk_message_type = models.ForeignKey(BulkMessageType, on_delete=models.SET_NULL, null=True, blank=True, db_column='bulk_message_type_id')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "sms_log_items"
    