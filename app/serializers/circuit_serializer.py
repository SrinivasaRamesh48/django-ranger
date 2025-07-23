from rest_framework import serializers
from app.models import Circuit
from app.serializers.circuit_carrier_serializer import CircuitCarrierSerializer
from app.serializers.us_state_serializer import UsStateSerializer

class CircuitSerializer(serializers.ModelSerializer):
    circuit_carrier = CircuitCarrierSerializer(read_only=True)
    state = UsStateSerializer(read_only=True)
    circuit_carrier_id = serializers.PrimaryKeyRelatedField(
        queryset=Circuit.objects.all(), source='circuit_carrier', write_only=True
    )
    state_id = serializers.PrimaryKeyRelatedField(
        queryset=Circuit.objects.all(), source='state', write_only=True
    )

    class Meta:
        model = Circuit
        fields = [
            'circuit_id', 
            'title', 
            'address', 
            'city', 
            'zip_code', 
            'circuit_id_a', 
            'circuit_id_z', 
            'contact_number', 
            'activation_date', 
            'mbps_speed', 
            'facility_assignment', 
            'media_type', 
            'circuit_carrier', 
            'circuit_carrier_id', 
            'state', 
            'state_id', 
            'created_at', 
            'updated_at'
        ]
