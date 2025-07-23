from rest_framework import serializers
from app.models import BulkMessageType


class BulkMessageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulkMessageType
        fields = ['bulk_message_type_id', 'description']
