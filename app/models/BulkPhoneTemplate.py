from django.db import models
from .BulkMessageType import BulkMessageType # Import the related model

class BulkPhoneTemplate(models.Model):
    bulk_phone_template_id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True, null=True) 
    bulk_message_type = models.ForeignKey(BulkMessageType, on_delete=models.CASCADE, db_column='bulk_message_type_id')
    body = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bulk_phone_templates'
        app_label = 'app' 
        
    def __str__(self):
        return f"Phone Template {self.bulk_phone_template_id} - {self.description or 'No description'}"