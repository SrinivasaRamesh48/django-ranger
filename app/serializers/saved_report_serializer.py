from rest_framework import serializers
from app.models import SavedReport, ReportType
from app.serializers.report_type_serializer import ReportTypeSerializer 

class SavedReportSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    report_type_id = serializers.PrimaryKeyRelatedField(queryset=ReportType.objects.all(), source='type', write_only=True)

    class Meta:
        model = SavedReport
        fields = '__all__'

    def get_type(self, obj):
        return ReportTypeSerializer(obj.type).data if obj.type else None   
