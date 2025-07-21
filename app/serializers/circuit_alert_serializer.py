from rest_framework import serializers
from app.models.circuit_alert import CircuitAlert
from app.serializers.alert_type_serializer import AlertTypeSerializer
from app.serializers.circuit_serializer import CircuitSerializer
from app.serializers.user_serializer import UserSerializer

class CircuitAlertSerializer(serializers.ModelSerializer):
    alert_type = AlertTypeSerializer()
    circuit = CircuitSerializer()
    activated_by = UserSerializer()
    deactivated_by = UserSerializer()
    updated_by = UserSerializer()

    class Meta:
        model = CircuitAlert
        fields = '__all__'