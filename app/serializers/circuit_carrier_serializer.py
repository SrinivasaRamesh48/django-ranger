from rest_framework import serializers
from app.models import CircuitCarrier


class CircuitCarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = CircuitCarrier
        fields = ['circuit_carrier_id', 'name']
