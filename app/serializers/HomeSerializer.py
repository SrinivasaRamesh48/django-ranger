from rest_framework import serializers
from app.models.Home import Home
# Import all related models and their serializers for nesting
from app.models.Project import Project
from app.models.UsState import UsState
from app.models.MacAddress import MacAddress
from app.models.Node import Node
from app.models.HomeAlert import HomeAlert # Import the HomeAlert model
from .UsStateSerializer import UsStateSerializer
from .MacAddressSerializer import MacAddressSerializer
from .NodeSerializer import NodeSerializer
from .UploadsSerializer import UploadsSerializer
from .UserSerializer import User


class HomeSerializer(serializers.ModelSerializer):
    
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all()) 
    state = UsStateSerializer(read_only=True) 
    mac_address = MacAddressSerializer(read_only=True) # Nested for MacAddress
    node = NodeSerializer(read_only=True) # Nested for Node
    wiring_certified_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True) # Or UserSerializer

    # HasMany relationships (nested serializers)
    mesh_installs = serializers.SerializerMethodField() # Custom method to apply whereNull('deleted_at')
    subscribers = serializers.SerializerMethodField() # Custom method to apply potential filters or just return all
    uploads = UploadsSerializer(many=True, read_only=True) # Assuming UploadsSerializer is defined
    alerts = serializers.SerializerMethodField() # Custom method for where and orderByDesc

    # Custom properties from Django Model
    active_subscriber = serializers.SerializerMethodField()
    port_mac_address_info = serializers.SerializerMethodField()

    class Meta:
        model = Home
        fields = '__all__' # Or specify the fields you want

    # # --- Methods for SerializerMethodField ---
    # def get_mesh_installs(self, obj):
    #     # Apply the Laravel filter: ->whereNull('deleted_at')
    #     # Assuming MeshCPEInstall model has a 'deleted_at' DateTimeField
    #     # and MeshCPEInstallSerializer is defined
    #     from .models.MeshCPEInstall import MeshCPEInstall
    #     from .serializers import MeshCPEInstallSerializer # Ensure this is defined
    #     qs = obj.mesh_installs.filter(deleted_at__isnull=True)
    #     return MeshCPEInstallSerializer(qs, many=True, read_only=True).data

    # def get_subscribers(self, obj):
    #     # Return all subscribers or apply filters if specific ones are expected here
    #     from .models.Subscriber import Subscriber
    #     from .serializers import SubscriberSerializer # Ensure this is defined
    #     return SubscriberSerializer(obj.subscribers.all(), many=True, read_only=True).data

    # def get_alerts(self, obj):
    #     # Apply the Laravel filter: ->where("active", 1)->orderByDesc('alert_type_id')
    #     from .models.HomeAlert import HomeAlert
    #     from .serializers import HomeAlertSerializer # Ensure this is defined
    #     qs = obj.home_alerts.filter(active=True).order_by('-alert_type_id')
    #     return HomeAlertSerializer(qs, many=True, read_only=True).data

    # def get_active_subscriber(self, obj):
    #     # Call the @property method defined in the Home model
    #     active_sub = obj.active_subscriber
    #     if active_sub:
    #         from .serializers import SubscriberSerializer # Ensure SubscriberSerializer is defined
    #         return SubscriberSerializer(active_sub, read_only=True).data
    #     return None

    # def get_port_mac_address_info(self, obj):
    #     # Call the @property method defined in the Home model
    #     port_mac_info = obj.port_mac_address_info
    #     if port_mac_info:
    #         from .serializers import PortMacAddressSerializer # Ensure PortMacAddressSerializer is defined
    #         return PortMacAddressSerializer(port_mac_info, read_only=True).data
    #     return None
    
    
class HomeAlertSerializer(serializers.ModelSerializer):
    # Optional: To display more than just the ID for foreign keys,
    # you can use fields like StringRelatedField or nest serializers.
    # For example:
    # alert_type = AlertTypeSerializer(read_only=True) # Nests the full alert type object
    # home = HomeSerializer(read_only=True) # Nests the full home object
    # activated_by = UserSerializer(read_only=True)
    # deactivated_by = UserSerializer(read_only=True)
    # updated_by = UserSerializer(read_only=True)

    class Meta:
        model = HomeAlert
        fields = '__all__'
        # Or specify fields explicitly if you don't want to expose all:
        # fields = [
        #     'home_alert_id', 'alert_type', 'home', 'message', 'active',
        #     'activated_by', 'deactivated_by', 'updated_by', 'created_at', 'updated_at'
        # ]
    