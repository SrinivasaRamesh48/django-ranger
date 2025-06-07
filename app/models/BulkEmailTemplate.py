from django.db import models
from .BulkMessageType import BulkMessageType

class BulkEmailTemplate(models.Model):
    bulk_email_template_id = models.AutoField(primary_key=True)
    description = models.TextField()
    bulk_message_type = models.ForeignKey(BulkMessageType, on_delete=models.CASCADE, db_column='bulk_message_type_id')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bulk_email_templates'
        app_label = 'app'  

    def __str__(self):
        return f"Template: {self.subject}" 