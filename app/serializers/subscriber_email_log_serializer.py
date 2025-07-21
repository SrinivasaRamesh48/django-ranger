from rest_framework import serializers
from app.models import SubscriberEmailLog, EmailLogItem, Subscriber
from app.serializers.email_log_item_serializer import EmailLogItemSerializer
from app.serializers.subscriber_serializer import SubscriberSerializer

class SubscriberEmailLogSerializer(serializers.ModelSerializer):
    item = EmailLogItemSerializer(read_only=True)
    subscriber = SubscriberSerializer(read_only=True)

    email_log_item_id = serializers.PrimaryKeyRelatedField(queryset=EmailLogItem.objects.all(), source='item', write_only=True)
    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)

    class Meta:
        model = SubscriberEmailLog
        fields = [
            'subscriber_email_log_id', 'sent_to', 'success', 
            'created_at', 'updated_at',
            'item', 'email_log_item_id',
            'subscriber', 'subscriber_id'
        ]  
