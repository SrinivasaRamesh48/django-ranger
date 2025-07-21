from rest_framework import serializers
from app.models import ReportType


class ReportTypeSerializer(serializers.ModelSerializer):
    saved_reports = serializers.SerializerMethodField()
    
    class Meta:
        model = ReportType
        fields = '__all__'

