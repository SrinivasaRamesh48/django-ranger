from rest_framework import serializers
from app.models import NodeFrame


class NodeFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeFrame
        fields = ['node_frame_id', 'description']
