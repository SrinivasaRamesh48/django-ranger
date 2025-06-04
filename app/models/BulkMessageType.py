from django.db import models

class BulkMessageType(models.Model):
    bulk_message_type_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255) # Assuming description is a string field

    class Meta:
        db_table = 'bulk_message_type'
        app_label = 'app' # Replace 'your_app_name' with the actual name of your Django app

    def __str__(self):
        return self.description # Returns the description for better readability