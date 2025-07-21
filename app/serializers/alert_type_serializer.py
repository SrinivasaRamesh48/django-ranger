from rest_framework import serializers
from app.models import AlertType


class AlertTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertType
        fields = ['alert_type_id', 'description']
