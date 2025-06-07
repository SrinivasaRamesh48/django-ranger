# app/serializers.py

from rest_framework import serializers
from app.models.Ont import Ont # Import the Ont model
from app.models.OntManufacturer import OntManufacturer

class OntSerializer(serializers.ModelSerializer):
    # Optional: If you want nested representations of related objects
    # node = NodeSerializer(read_only=True)
    # manufacturer = OntManufacturerSerializer(read_only=True)
    # home = HomeSerializer(read_only=True) # For the OneToOneField

    class Meta:
        model = Ont
        fields = '__all__'
        # Or specify explicit fields if you don't want to expose all:
        # fields = [
        #     'ont_id', 'node', 'ont_manufacturer', 'home', 'fsan', 'mac_address',
        #     'serial_number', 'interface', 'model_id', 'ont_version',
        #     'software_version', 'ont_rx_power', 'olt_rx_power', 'distance',
        #     'last_pulled', 'created_at', 'updated_at'
        # ]
        
        
class OntManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OntManufacturer
        fields = '__all__'
              