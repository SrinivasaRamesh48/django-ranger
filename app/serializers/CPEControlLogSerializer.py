from rest_framework import serializers
from app.models.CPEControlLog import CPEControlLog
from app.models.CPEControlLogType import CPEControlLogType


class CPEControlLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPEControlLog
        fields = '__all__'
        
        
class CPEControlLogTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPEControlLogType
        fields = '__all__'