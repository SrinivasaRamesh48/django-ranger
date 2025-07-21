from rest_framework import serializers
from app.models import Circuit


class CircuitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circuit
        fields = ['circuit_id', 'title']
