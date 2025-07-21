from rest_framework import serializers
from app.models import Statement, Subscriber
from app.serializers.statement_item_serializer import StatementItemSerializer

class StatementSerializer(serializers.ModelSerializer):
    """Serializes Statement instances for API responses."""
    subscriber = serializers.SerializerMethodField()
    items = StatementItemSerializer(many=True, read_only=True)
    
    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)

    def get_subscriber(self, obj):
        from app.serializers.subscriber_serializer import SubscriberSerializer
        return SubscriberSerializer(obj.subscriber).data if obj.subscriber else None

    class Meta:
        model = Statement
        fields = '__all__'
