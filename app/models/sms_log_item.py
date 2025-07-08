from django.db import models
from .time_stamped_model_mixin import TimeStampedModelMixin  
class SMSLogItem(TimeStampedModelMixin, models.Model):
    sms_log_item_id = models.AutoField(primary_key=True)
    body = models.TextField()
    outage = models.ForeignKey('Outage', on_delete=models.SET_NULL, null=True, blank=True, db_column='outage_id')
    bulk_message_type = models.ForeignKey('BulkMessageType', on_delete=models.SET_NULL, null=True, blank=True, db_column='bulk_message_type_id')


    class Meta:
        db_table = "sms_log_items"
        app_label = 'app'