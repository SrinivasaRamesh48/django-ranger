# app/serializers.py

from rest_framework import serializers
from app.models.SMSLogItem import SMSLogItem # Import the SMSLogItem model

# Optional: If you want nested representations of related objects:
# from .serializers import OutageSerializer, BulkMessageTypeSerializer

# ... (your other serializers) ...

class SMSLogItemSerializer(serializers.ModelSerializer):
    # Optional: For nested representations
    # outage = OutageSerializer(read_only=True)
    # bulk_message_type = BulkMessageTypeSerializer(read_only=True)

    class Meta:
        model = SMSLogItem
        fields = '__all__'
        # Or specify explicit fields if you don't want to expose all:
        # fields = [
        #     'sms_log_item_id', 'body', 'outage', 'bulk_message_type',
        #     'created_at', 'updated_at'
        # ]