from rest_framework import serializers
from app.models import OltSnapshot, Node
from app.serializers.node_serializer import NodeSerializer


class OltSnapshotSerializer(serializers.ModelSerializer):
    node = NodeSerializer(read_only=True)
    node_id = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all(), source='node', write_only=True)
    
    class Meta:
        model = OltSnapshot
        fields = [
            'id', 'olt_ip_address', 'interface', 'fsan', 'ont_model', 'ont_active_version', 
            'ont_standby_version', 'ont_rx_power', 'ont_tx_power', 'distance', 'created_at',
            'node', 'node_id'
        ]
