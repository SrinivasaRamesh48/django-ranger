from rest_framework import serializers
from app.models.ReportType import ReportType

class ReportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportType
        fields = '__all__'
