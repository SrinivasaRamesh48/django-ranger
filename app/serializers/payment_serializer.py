from rest_framework import serializers
from app.models import Payment
from app.serializers.subscriber_payment_method_serializer import SubscriberPaymentMethodSerializer

class PaymentSerializer(serializers.ModelSerializer):
    subscriber = serializers.SerializerMethodField()
    statement = serializers.SerializerMethodField()
    payment_method = SubscriberPaymentMethodSerializer(read_only=True)

    def get_subscriber(self, obj):
        if obj.subscriber:
            # Import here to avoid circular import
            from app.serializers.subscriber_serializer import SubscriberSerializer
            return SubscriberSerializer(obj.subscriber).data
        return None

    def get_statement(self, obj):
        if obj.statement:
            # Import here to avoid circular import
            from app.serializers.statement_serializer import StatementSerializer
            return StatementSerializer(obj.statement).data
        return None

    class Meta:
        model = Payment
        fields = [
            'payment_id', 'amount', 'merchant_id', 'autopay_merchant_id', 'qbo_payment_id',
            'created_at', 'updated_at',
            'subscriber', 
            'statement', 
            'payment_method'
        ]
