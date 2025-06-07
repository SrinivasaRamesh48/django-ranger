# app/serializers.py

from rest_framework import serializers
from app.models.PortMacAddress import PortMacAddress
# Import serializers for nested relationships if you want them in the API response:
# from .serializers import NodeSerializer # Assuming NodeSerializer is defined
# from .serializers import MacAddressSerializer # Assuming MacAddressSerializer is defined
# from .serializers import HomeSerializer # Assuming HomeSerializer is defined

# ... (your other serializers) ...

class PortMacAddressSerializer(serializers.ModelSerializer):
    # Optional: For nested representations of related objects
    # node = NodeSerializer(read_only=True)
    # mac_address_found = MacAddressSerializer(read_only=True) # Nested for the property lookup

    # Use SerializerMethodField for custom properties
    home_found = serializers.SerializerMethodField() # For the home_found_info property

    class Meta:
        model = PortMacAddress
        fields = '__all__'
        # You might explicitly list fields to control order or exclude some
        # fields = [
        #     'id', 'node', 'node_switch_unit', 'node_switch_module', 'mac_address',
        #     'created_at', 'updated_at', 'node_port_vlanid', 'node_oper_status',
        #     'node_admin_status', 'node_rate_up', 'node_rate_down',
        #     'home_found', # Include the custom property
        #     'mac_address_found', # Include the custom property (auto-generated from model property)
        # ]

    def get_home_found(self, obj):
        home_instance = obj.home_found_info
        if home_instance:
            # Assuming HomeSerializer is defined and imported
            from .serializers import HomeSerializer # Import locally to avoid circular dependencies
            return HomeSerializer(home_instance).data
        return None