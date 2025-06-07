# app/serializers.py

from rest_framework import serializers
from app.models.EmailLogItem import EmailLogItem # Import the EmailLogItem model
# from .serializers import OutageSerializer, BulkMessageTypeSerializer # Uncomment and define these if you want nested output

# ... (your other serializers) ...

class EmailLogItemSerializer(serializers.ModelSerializer):
    # Optional: If you want nested representations of Outage and BulkMessageType
    # outage = OutageSerializer(read_only=True)
    # bulk_message_type = BulkMessageTypeSerializer(read_only=True)

    class Meta:
        model = EmailLogItem
        fields = '__all__'
        # Or specify explicit fields if you don't want to expose all:
        # fields = [
        #     'email_log_item_id', 'subject', 'body', 'outage',
        #     'bulk_message_type', 'created_at', 'updated_at'
        # ]