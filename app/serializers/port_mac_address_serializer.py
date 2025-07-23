from rest_framework import serializers
from app.models import PortMacAddress, Node
from app.serializers.node_serializer import NodeSerializer
from app.serializers.mac_address_serializer import MacAddressSerializer
from app.serializers.home_serializer import HomeSerializer

class PortMacAddressSerializer(serializers.ModelSerializer):
    node = NodeSerializer(read_only=True)
    mac_address_found = serializers.SerializerMethodField()
    home_found = serializers.SerializerMethodField()

    class Meta:
        model = PortMacAddress
        fields = [
            'PortMacAddress_id',
            'node',
            'node_switch_unit',
            'node_switch_module',
            'mac_address',
            'node_port_vlanid',
            'node_oper_status',
            'node_admin_status',
            'node_rate_up',
            'node_rate_down',
            'created_at',
            'mac_address_found',
            'home_found',
        ]

    def get_mac_address_found(self, obj):
        mac = obj.mac_address_found
        return MacAddressSerializer(mac).data if mac else None

    def get_home_found(self, obj):
        home = obj.home_found
        return HomeSerializer(home).data if home else None