from rest_framework import serializers
from app.models import PasswordResetToken, Subscriber


class PasswordResetTokenSerializer(serializers.ModelSerializer):
    subscriber = serializers.SerializerMethodField()
    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)

    class Meta:
        model = PasswordResetToken
        fields = [
            'password_reset_token_id', 'token', 'expires',
            'subscriber', 'subscriber_id',
            'created_at', 'updated_at'
        ]
        
    def get_subscriber(self, obj):
        from app.serializers.subscriber_serializer import SubscriberSerializer
        return SubscriberSerializer(obj.subscriber).data if obj.subscriber else None
