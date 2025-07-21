from rest_framework import serializers
from app.models import Payment, Subscriber, Statement, SubscriberPaymentMethod


class PaymentSerializer(serializers.ModelSerializer):
    subscriber = serializers.SerializerMethodField()
    # statement = StatementSerializer(read_only=True)
    # payment_method = SubscriberPaymentMethodSerializer(read_only=True)

    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)
    statement_id = serializers.PrimaryKeyRelatedField(queryset=Statement.objects.all(), source='statement', write_only=True)
    subscriber_payment_method_id = serializers.PrimaryKeyRelatedField(queryset=SubscriberPaymentMethod.objects.all(), source='payment_method', write_only=True)

    def get_subscriber(self, obj):
        from app.serializers.subscriber_serializer import SubscriberSerializer
        return SubscriberSerializer(obj.subscriber).data if obj.subscriber else None

    class Meta:
        model = Payment
        fields = [
            'payment_id', 'amount', 'merchant_id', 'autopay_merchant_id', 'qbo_payment_id',
            'created_at', 'updated_at',
            'subscriber', 'subscriber_id',
            'statement', 'statement_id',
            'payment_method', 'subscriber_payment_method_id'
        ]
