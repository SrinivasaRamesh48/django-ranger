from rest_framework import serializers
from app.models import Outage
from app.serializers.project_serializer import ProjectSerializer
from app.models import Project
from app.serializers.outage_homes_effected_serializer import OutageHomesEffectedSerializer
from app.serializers.alert_serializer import AlertSerializer

class OutageSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), source='project', write_only=True
    )
    alert = AlertSerializer(read_only=True, many=True)
    effected = OutageHomesEffectedSerializer(many=True, read_only=True)
    class Meta:
        model = Outage
        fields = [
            'outage_id',
            'project', 'project_id',
            'resolved',
            'email_notices_sent',
            'phone_notices_sent',
            'phone_message_updated',
            'confirmed',
            'confirmed_at',
            'created_at',
            'updated_at',
            'created_at', 'updated_at',
            'alert',
            'effected'
        ]

    