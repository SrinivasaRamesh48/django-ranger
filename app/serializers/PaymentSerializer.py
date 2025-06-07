# app/serializers.py

from rest_framework import serializers
from app.models.Payment import Payment # Import the Payment model

# Optional: If you want nested representations of related objects:
# from .serializers import SubscriberSerializer, StatementSerializer, SubscriberPaymentMethodSerializer

# ... (your other serializers) ...

class PaymentSerializer(serializers.ModelSerializer):
    # Optional: For nested representations
    # subscriber = SubscriberSerializer(read_only=True)
    # statement = StatementSerializer(read_only=True)
    # payment_method = SubscriberPaymentMethodSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
        # Or specify explicit fields:
        # fields = [
        #     'payment_id', 'subscriber', 'statement', 'amount', 'merchant_id',
        #     'payment_method', 'autopay_merchant_id', 'qbo_payment_id',
        #     'created_at', 'updated_at'
        # ]