from rest_framework import serializers
from app.models.MacAddress import MacAddress
from app.models.MacAddressLookup import MacAddressLookup

class MacAddressLookupSerializer(serializers.ModelSerializer):
    """Serializes the manufacturer information."""
    class Meta:
        model = MacAddressLookup
        fields = ['manufacturer']


class MacAddressSerializer(serializers.ModelSerializer):
    """
    Serializer for the MacAddress model.
    """
    # Use a nested serializer to display manufacturer details from our custom property.
    # The 'source' argument points to the @property method on the model.
    manufacturer = MacAddressLookupSerializer(read_only=True)

    # This field will call the `get_default_credentials` method below.
    default_credentials = serializers.SerializerMethodField()

    class Meta:
        model = MacAddress
        fields = [
            'mac_address_id',
            'address',
            'home',  
            'cpe_serial_number',
            'firmware_update',
            'firmware_update_manual',
            'created_at',
            # Custom-logic fields
            'manufacturer',
            'default_credentials'
        ]
        # We exclude the raw encrypted fields from the API response for security.
        read_only_fields = ['manufacturer', 'default_credentials']

    def get_default_credentials(self, obj):
        """
        This method is called by the 'default_credentials' SerializerMethodField.
        It simply returns the value from the model's @property.
        """
        return obj.default_credentials