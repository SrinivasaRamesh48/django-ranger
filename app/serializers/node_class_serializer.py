from rest_framework import serializers
from app.models import NodeClass


class NodeClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeClass
        fields = ['node_class_id', 'description', 'created_at', 'updated_at']
