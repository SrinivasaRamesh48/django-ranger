from rest_framework import serializers
from app.models import Alert, AlertType, User, Outage
from app.serializers.alert_type_serializer import AlertTypeSerializer
from app.serializers.user_serializer import UserSerializer


class AlertSerializer(serializers.ModelSerializer):
    alert_type = AlertTypeSerializer(read_only=True)
    activated_by = UserSerializer(read_only=True)
    deactivated_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    
    
    alert_type_id = serializers.PrimaryKeyRelatedField(queryset=AlertType.objects.all(), source='alert_type', write_only=True)
    activated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='activated_by', write_only=True, required=False, allow_null=True)
    deactivated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='deactivated_by', write_only=True, required=False, allow_null=True)
    updated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='updated_by', write_only=True, required=False, allow_null=True)
    outage_id = serializers.PrimaryKeyRelatedField(queryset=Outage.objects.all(), source='outage', write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Alert
        fields = [
            'alert_id', 'message', 'active', 'alert_type', 'alert_type_id',
            'activated_by', 'activated_by_id', 'deactivated_by', 'deactivated_by_id',
            'updated_by', 'updated_by_id', 'outage_id', 'created_at', 'updated_at'
        ]
