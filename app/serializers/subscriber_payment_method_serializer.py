from rest_framework import serializers
from app.models import SubscriberPaymentMethod, Subscriber

class SubscriberPaymentMethodSerializer(serializers.ModelSerializer):
    subscriber = serializers.SerializerMethodField()
    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)

    def get_subscriber(self, obj):
        from app.serializers.subscriber_serializer import SubscriberSerializer
        return SubscriberSerializer(obj.subscriber).data if obj.subscriber else None

    class Meta:
        model = SubscriberPaymentMethod
        fields = [
            'subscriber_payment_method_id', 'nickname', 'card_exp_datetime', 
            'merchant_payment_method_id', 'created_at', 'updated_at',
            'subscriber', 'subscriber_id'
        ]
