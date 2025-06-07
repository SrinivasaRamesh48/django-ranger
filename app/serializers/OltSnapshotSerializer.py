# app/serializers.py

from rest_framework import serializers
from app.models.OltSnapshot import OltSnapshot # Import the OltSnapshot model

class OltSnapshotSerializer(serializers.ModelSerializer):
    # Example of nesting related objects (uncomment and define serializers if needed):
    # node = NodeSerializer(read_only=True)
    # manufacturer = OntManufacturerSerializer(read_only=True) # If OntManufacturer model exists and is related
    # home = HomeSerializer(read_only=True) # If Home model exists and is related

    class Meta:
        model = OltSnapshot
        fields = '__all__' # This includes all fields: id, node, olt_ip_address, interface, fsan, ont_model, ont_active_version, ont_standby_version, ont_rx_power, ont_tx_power, distance, created_at, updated_at
        # Or specify fields explicitly if you don't want to expose all:
        # fields = [
        #     'id', 'node', 'olt_ip_address', 'interface', 'fsan', 'ont_model',
        #     'ont_active_version', 'ont_standby_version', 'ont_rx_power',
        #     'ont_tx_power', 'distance', 'created_at', 'updated_at'
        # ]