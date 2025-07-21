from rest_framework import serializers
from app.models import CPEControlLogType


class CPEControlLogTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPEControlLogType
        fields = ['cpe_control_log_type_id', 'name']
