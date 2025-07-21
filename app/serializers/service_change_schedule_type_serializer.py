from rest_framework import serializers
from app.models import ServiceChangeScheduleType


class ServiceChangeScheduleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceChangeScheduleType
        fields = ['__all__']
