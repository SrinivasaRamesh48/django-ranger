from rest_framework import serializers
from app.models import PortMacAddress, Node
from app.serializers.node_serializer import NodeSerializer
from app.serializers.mac_address_serializer import MacAddressSerializer
from app.serializers.home_serializer import HomeSerializer

class PortMacAddressSerializer(serializers.ModelSerializer):
    node = NodeSerializer(read_only=True)
    mac_address_found = MacAddressSerializer(read_only=True)
    home_found = HomeSerializer(read_only=True)

    node_Id = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all(), source='node', write_only=True)

    class Meta:
        model = PortMacAddress
        fields = [
            'id', 'node_Id', 'node_switch_unit', 'node_switch_module', 'mac_address',
            'node_port_vlanid', 'node_oper_status', 'node_admin_status', 'node_rate_up',
            'node_rate_down', 'created_at',
            'node', 'mac_address_found', 'home_found'
        ]
