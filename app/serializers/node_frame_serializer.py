from rest_framework import serializers
from app.models import NodeFrame


class NodeFrameSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    def get_project(self, obj):
        if obj.project:
            from app.serializers.project_serializer import ProjectSerializer
            return ProjectSerializer(obj.project).data
        return None

    class Meta:
        model = NodeFrame
        fields = ['node_frame_id', 'description', 'project', 'created_at', 'updated_at']
