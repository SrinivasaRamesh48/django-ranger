from rest_framework import serializers
from app.models import StatementItem, StatementItemDescription, Payment
from app.serializers.statement_item_description_serializer import StatementItemDescriptionSerializer

class StatementItemSerializer(serializers.ModelSerializer):
    description = StatementItemDescriptionSerializer(read_only=True)
    payment = serializers.SerializerMethodField()

    statement_item_description_id = serializers.PrimaryKeyRelatedField(queryset=StatementItemDescription.objects.all(), source='description', write_only=True)
    payment_id = serializers.PrimaryKeyRelatedField(queryset=Payment.objects.all(), source='payment', write_only=True, required=False, allow_null=True)

    def get_payment(self, obj):
        if obj.payment:
            # Import here to avoid circular import
            from app.serializers.payment_serializer import PaymentSerializer
            return PaymentSerializer(obj.payment).data
        return None

    class Meta:
        model = StatementItem
        fields = '__all__'
