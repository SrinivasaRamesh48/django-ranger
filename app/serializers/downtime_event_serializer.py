from rest_framework import serializers
from app.models import DowntimeEvent, Outage, Project


class DowntimeEventSerializer(serializers.ModelSerializer):
    outage = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()
    outage_id = serializers.PrimaryKeyRelatedField(queryset=Outage.objects.all(), source='outage', write_only=True)
    project_id = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), source='project', write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = DowntimeEvent
        fields = [
            'downtime_event_id', 'created_at', 'updated_at',
            'outage', 'project',
            'outage_id', 'project_id',
        ]
        
    def get_outage(self, obj):
        from app.serializers.outage_serializer import OutageSerializer
        return OutageSerializer(obj.outage).data if obj.outage else None
        
    def get_project(self, obj):
        from app.serializers.project_serializer import ProjectSerializer
        return ProjectSerializer(obj.project).data if obj.project else None
