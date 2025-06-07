from rest_framework import serializers
from app.models.Node import Node
from app.models.NodeClass import NodeClass
from app.models.NodeFrame import NodeFrame
from app.models.NodeType import NodeType


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'

class NodeClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeClass
        fields = '__all__'

class NodeFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeFrame
        fields = '__all__'

class NodeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeType
        fields = '__all__'