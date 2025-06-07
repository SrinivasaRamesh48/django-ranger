from rest_framework import serializers
from app.models.MacAddress import MacAddress
from app.models.MacAddressLookup import MacAddressLookup
# from .serializers import HomeSerializer # If you want nested Home representation

# class MacAddressLookupSerializer(serializers.ModelSerializer):  # If you have a MacAddressLookup model
#     class Meta:
#         model = MacAddressLookup
#         fields = '__all__'

class MacAddressSerializer(serializers.ModelSerializer):
    # home = HomeSerializer(read_only=True) # If you want nested Home representation
    manufacturer = serializers.SerializerMethodField()
    default_credentials = serializers.SerializerMethodField()

    class Meta:
        model = MacAddress
        fields = '__all__'

    def get_manufacturer(self, obj):
        manufacturer = obj.manufacturer
        if manufacturer:
            # Assuming you have a MacAddressLookupSerializer
            # from .serializers import MacAddressLookupSerializer
            # return MacAddressLookupSerializer(manufacturer).data
            return str(manufacturer)  # Or return a string representation if you don't have a serializer
        return None

    def get_default_credentials(self, obj):
         return obj.default_credentials_info


class MacAddressLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MacAddressLookup
        fields = '__all__' # This will include all fields from the model
        # Or explicitly list them:
        # fields = ['mac_address_lookup_id', 'mac_prefix', 'manufacturer_name']     