from rest_framework import serializers
from app.models import Outage
from app.serializers.project_serializer import ProjectSerializer
from app.serializers.home_serializer import HomeSerializer
from app.serializers.alert_serializer import AlertSerializer
from app.models import Project

class OutageSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    effected_homes = HomeSerializer(many=True, read_only=True)
    alert = AlertSerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), source='project', write_only=True)
    class Meta:
        model = Outage
        fields = '__all__'
