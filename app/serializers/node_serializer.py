from rest_framework import serializers
from app.models import Node
from app.serializers.node_frame_serializer import NodeFrameSerializer
from app.serializers.node_type_serializer import NodeTypeSerializer
from app.serializers.node_class_serializer import NodeClassSerializer
from app.serializers.project_serializer import ProjectSerializer
from app.serializers.home_serializer import HomeSerializer


class NodeSerializer(serializers.ModelSerializer):
    node_frame = NodeFrameSerializer(read_only=True)
    node_type = NodeTypeSerializer(read_only=True)
    node_class = NodeClassSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    node_frame_id = serializers.PrimaryKeyRelatedField(
        queryset=Node.objects.all(), source='node_frame', write_only=True
    )
    node_type_id = serializers.PrimaryKeyRelatedField(
        queryset=Node.objects.all(), source='node_type', write_only=True
    )
    node_class_id = serializers.PrimaryKeyRelatedField(
        queryset=Node.objects.all(), source='node_class', write_only=True
    )   
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Node.objects.all(), source='project', write_only=True
    )
    home = HomeSerializer(many=True, read_only=True)
    class Meta:
        model = Node
        fields = [
            'node_id', 
            'hostname', 
            'ip_address', 
            'mac_address', 
            'serial_number', 
            'dns_ip_address', 
            'active', 
            'node_frame', 
            'node_type', 
            'node_class', 
            'project',
            'node_frame_id', 
            'node_type_id', 
            'node_class_id', 
            'project_id',
            'created_at', 
            'updated_at',
            'home'
        ]
