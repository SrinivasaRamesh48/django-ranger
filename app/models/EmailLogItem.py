from django.db import models
from .Outage import Outage
from .BulkMessageType import BulkMessageType 


class EmailLogItem(models.Model):
    """Django equivalent of the Laravel EmailLogItem model."""
    email_log_item_id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    outage = models.ForeignKey(Outage, on_delete=models.SET_NULL, null=True, blank=True, db_column='outage_id')
    bulk_message_type = models.ForeignKey(BulkMessageType, on_delete=models.SET_NULL, null=True, blank=True, db_column='bulk_message_type_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "email_log_items"
        ordering = ['-created_at']
    def __str__(self):
        return self.subject
    email_log_item_id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    outage = models.ForeignKey(
        Outage,
        on_delete=models.SET_NULL, # Assuming email logs might remain even if outage is deleted
        null=True, blank=True,
        db_column='outage_id',
        related_name='email_log_items'
    )
    bulk_message_type = models.ForeignKey(
        BulkMessageType,
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        db_column='bulk_message_type_id',
        related_name='email_log_items'
    )


    class Meta:
        db_table = 'email_log_items'
        app_label = 'app'

    def __str__(self):
        return f"Email Log Item {self.email_log_item_id} - {self.subject}"