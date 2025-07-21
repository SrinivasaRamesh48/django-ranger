from rest_framework import serializers
from app.models import EmailLogItem, Outage, BulkMessageType
from app.serializers.outage_serializer import OutageSerializer
from app.serializers.bulk_message_type_serializer import BulkMessageTypeSerializer


class EmailLogItemSerializer(serializers.ModelSerializer):
    outage = OutageSerializer(read_only=True)
    bulk_message_type = BulkMessageTypeSerializer(read_only=True)
    outage_id = serializers.PrimaryKeyRelatedField(queryset=Outage.objects.all(), source='outage', write_only=True, required=False, allow_null=True)
    bulk_message_type_id = serializers.PrimaryKeyRelatedField(queryset=BulkMessageType.objects.all(), source='bulk_message_type', write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = EmailLogItem
        fields = [
            'email_log_item_id', 'subject', 'body', 'created_at', 'updated_at',
            'outage', 'bulk_message_type',
            'outage_id', 'bulk_message_type_id'
        ]
