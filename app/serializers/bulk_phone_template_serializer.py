from rest_framework import serializers
from app.models import BulkPhoneTemplate, BulkMessageType
from app.serializers.bulk_message_type_serializer import BulkMessageTypeSerializer


class BulkPhoneTemplateSerializer(serializers.ModelSerializer):
    message_type = BulkMessageTypeSerializer(read_only=True)
    bulk_message_type_id = serializers.PrimaryKeyRelatedField(queryset=BulkMessageType.objects.all(), source='message_type', write_only=True)
    
    class Meta:
        model = BulkPhoneTemplate
        fields = [
            'bulk_phone_template_id', 'description', 'body',
            'message_type', 'bulk_message_type_id', 'active', 'created_at', 'updated_at'
        ]
