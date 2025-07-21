from rest_framework import serializers
from app.models import NodeType


class NodeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeType
        fields = ['node_type_id', 'description']
