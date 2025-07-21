from rest_framework import serializers
from app.models import Uploads
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

    class Meta:
        model = Uploads
        fields = '__all__'
