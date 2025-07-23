from rest_framework import serializers
from app.models import Uploads
from app.models.circuit import Circuit
from app.models.project import Project
from app.models.subscriber import Subscriber
from app.models.upload_types import UploadType
from app.models.home import Home
from app.serializers.project_serializer import ProjectSerializer
from app.serializers.circuit_serializer import CircuitSerializer
from app.serializers.upload_type_serializer import UploadTypeSerializer
from app.serializers.home_serializer import HomeSerializer
from app.serializers.subscriber_serializer import SubscriberSerializer

class UploadSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    circuit = CircuitSerializer(read_only=True)
    home = HomeSerializer(read_only=True)
    subscriber = SubscriberSerializer(read_only=True)
    upload_type = UploadTypeSerializer(read_only=True)
    
    
    project_id = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), source='project', write_only=True)
    circuit_id = serializers.PrimaryKeyRelatedField(queryset=Circuit.objects.all(), source='circuit', write_only=True)
    home_id = serializers.PrimaryKeyRelatedField(queryset=Home.objects.all(), source='home', write_only=True)
    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)
    upload_type_id = serializers.PrimaryKeyRelatedField(queryset=UploadType.objects.all(), source='upload_type', write_only=True)
    class Meta:
        model = Uploads
        fields = [
            'upload_id',
            'name',
            'path',
            'created_at',
            'updated_at',
            'project',
            'circuit',
            'home',
            'subscriber',
            'upload_type',
            'project_id',
            'circuit_id',
            'home_id',
            'subscriber_id',
            'upload_type_id'
        ]
