from rest_framework import serializers
from app.models import SubscriberAlert, AlertType, Subscriber, User
from app.serializers.alert_type_serializer import AlertTypeSerializer
from app.serializers.user_serializer import UserSerializer

class SubscriberAlertSerializer(serializers.ModelSerializer):
    alert_type = AlertTypeSerializer(read_only=True)
    subscriber = serializers.SerializerMethodField()
    activated_by = UserSerializer(read_only=True)
    deactivated_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    alert_type_id = serializers.PrimaryKeyRelatedField(queryset=AlertType.objects.all(), source='alert_type', write_only=True)
    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)
    activated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='activated_by', write_only=True, required=False, allow_null=True)
    deactivated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='deactivated_by', write_only=True, required=False, allow_null=True)
    updated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='updated_by', write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = SubscriberAlert
        fields = [
            'subscriber_alert_id', 'message', 'active', 'created_at', 'updated_at',
            'alert_type', 'subscriber', 'activated_by', 'deactivated_by', 'updated_by',
            'alert_type_id', 'subscriber_id', 'activated_by_id', 'deactivated_by_id', 'updated_by_id'
        ]

    def get_subscriber(self, obj):
        from app.serializers.subscriber_serializer import SubscriberSerializer
        return SubscriberSerializer(obj.subscriber).data if obj.subscriber else None
