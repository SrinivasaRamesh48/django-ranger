from rest_framework import serializers
from app.models import PasswordResetToken
from app.serializers.subscriber_serializer import SubscriberSerializer
from app.models import Subscriber

class PasswordResetTokenSerializer(serializers.ModelSerializer):
    subscriber = SubscriberSerializer(read_only=True)
    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)

    class Meta:
        model = PasswordResetToken
        fields = [
            'password_reset_token_id', 'token', 'expires',
            'subscriber', 'subscriber_id',
            'created_at', 'updated_at'
        ]