from rest_framework import serializers
from app.models import SubscriberSMSLog, SMSLogItem, Subscriber
from app.serializers.sms_log_item_serializer import SMSLogItemSerializer
from app.serializers.subscriber_serializer import SubscriberSerializer

class SubscriberSMSLogSerializer(serializers.ModelSerializer):
    item = SMSLogItemSerializer(read_only=True)
    subscriber = SubscriberSerializer(read_only=True)

    sms_log_item_id = serializers.PrimaryKeyRelatedField(queryset=SMSLogItem.objects.all(), source='item', write_only=True)
    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)

    class Meta:
        model = SubscriberSMSLog
        fields = [
            'subscriber_sms_log_id', 'sent_to', 'success', 
            'created_at', 'updated_at',
            'item', 'sms_log_item_id',
            'subscriber', 'subscriber_id'
        ]
