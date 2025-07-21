from rest_framework import serializers
from app.models import Ont, Home, Node, OntManufacturer


class OntSerializer(serializers.ModelSerializer):
    """Serializes Ont instances for API responses."""
    home = serializers.SerializerMethodField()
    node = serializers.SerializerMethodField()
    manufacturer = serializers.SerializerMethodField()

    home_id = serializers.PrimaryKeyRelatedField(queryset=Home.objects.all(), source='home', write_only=True)
    node_id = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all(), source='node', write_only=True)
    ont_manufacturer_id = serializers.PrimaryKeyRelatedField(queryset=OntManufacturer.objects.all(), source='manufacturer', write_only=True)

    class Meta:
        model = Ont
        fields = [
            'ont_id', 'fsan', 'mac_address', 'serial_number', 'interface', 'model_id',
            'ont_version', 'software_version', 'ont_rx_power', 'olt_rx_power',
            'distance', 'last_pulled', 'created_at', 'updated_at',
            'home', 'home_id',
            'node', 'node_id',
            'manufacturer', 'ont_manufacturer_id'
        ]        

    def get_home(self, obj):
        from app.serializers.home_serializer import HomeSerializer
        return HomeSerializer(obj.home).data if obj.home else None
        
    def get_node(self, obj):
        from app.serializers.node_serializer import NodeSerializer
        return NodeSerializer(obj.node).data if obj.node else None
        
    def get_manufacturer(self, obj):
        from app.serializers.ont_manufacturer_serializer import OntManufacturerSerializer
        return OntManufacturerSerializer(obj.manufacturer).data if obj.manufacturer else None
