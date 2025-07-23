from rest_framework import serializers
from app.models import NodeFrame
from app.serializers.project_serializer import ProjectSerializer

class NodeFrameSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = NodeFrame
        fields = ['node_frame_id', 'description', 'project', 'created_at', 'updated_at']
