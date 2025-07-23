from rest_framework import serializers
from app.models.alert_type import AlertType
from app.models.circuit_alert import CircuitAlert
from app.models.circuit import Circuit
from app.serializers.alert_type_serializer import AlertTypeSerializer
from app.serializers.circuit_serializer import CircuitSerializer
from app.serializers.user_serializer import UserSerializer
from test_circuit_alert_viewset import User

class CircuitAlertSerializer(serializers.ModelSerializer):
    alert_type = AlertTypeSerializer(read_only=True)
    circuit = CircuitSerializer(read_only=True)
    activated_by = UserSerializer(read_only=True)
    deactivated_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    alert_type_id = serializers.PrimaryKeyRelatedField(queryset=AlertType.objects.all(), source='alert_type', write_only=True)
    circuit_id = serializers.PrimaryKeyRelatedField(queryset=Circuit.objects.all(), source='circuit', write_only=True)
    activated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='activated_by', write_only=True, allow_null=True)
    deactivated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='deactivated_by', write_only=True, allow_null=True)
    updated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='updated_by', write_only=True, allow_null=True)

    class Meta:
        model = CircuitAlert
        fields = [
            'circuit_alert_id',
            'alert_type',
            'alert_type_id',
            'circuit',
            'circuit_id',
            'activated_by',
            'activated_by_id',
            'deactivated_by',
            'deactivated_by_id',
            'updated_by',
            'updated_by_id',
            'activated_at',
            'deactivated_at',
            'created_at',
            'updated_at',
        ]