from rest_framework import serializers
from app.models import BulkEmailTemplate, BulkMessageType
from app.serializers.bulk_message_type_serializer import BulkMessageTypeSerializer


class BulkEmailTemplateSerializer(serializers.ModelSerializer):
    message_type = BulkMessageTypeSerializer(read_only=True)
    bulk_message_type_id = serializers.PrimaryKeyRelatedField(queryset=BulkMessageType.objects.all(), source='message_type', write_only=True)
    
    class Meta:
        model = BulkEmailTemplate
        fields = [
            'bulk_email_template_id', 'description', 'subject', 'body',
            'message_type', 'bulk_message_type_id', 'created_at', 'updated_at'
        ]
