# app/serializers.py

from rest_framework import serializers
from django.db.models import F, Case, When, Value, IntegerField # For orderByRaw CONVERT(unit, SIGNED)
from app.models.ProjectAlert import ProjectAlert
from app.models.ProjectNetworkType import ProjectNetworkType
from app.models.Project import Project
# Import all related models and their serializers for nesting
from app.models.UsState import UsState
from app.models.Builder import Builder
from app.models.SubscriptionType import SubscriptionType
from app.models.ServicePlan import ServicePlan
from app.models.Circuit import Circuit
from app.models.ProjectNetworkType import ProjectNetworkType

# For hasMany relationships (if you want them nested)
# from app.models.Home import Home
# from app.models.Node import Node
# from app.models.NodeFrame import NodeFrame
# from app.models.Uploads import Uploads
# from app.models.ProjectAlert import ProjectAlert
# from app.models.AlertType import AlertType # For ProjectAlert nesting

# --- Nested Serializers (ensure these are defined above ProjectSerializer) ---
# Assuming these serializers exist from previous steps or you'll create them:
# class UsStateSerializer(serializers.ModelSerializer): ...
# class BuilderSerializer(serializers.ModelSerializer): ...
# class SubscriptionTypeSerializer(serializers.ModelSerializer): ...
# class ServicePlanSerializer(serializers.ModelSerializer): ...
# class CircuitSerializer(serializers.ModelSerializer): ...
# class ProjectNetworkTypeSerializer(serializers.ModelSerializer): ...

# For hasMany relationships with custom logic:
# class HomeSerializer(serializers.ModelSerializer): ...
# class NodeSerializer(serializers.ModelSerializer): ...
# class NodeFrameSerializer(serializers.ModelSerializer): ...
# class UploadsSerializer(serializers.ModelSerializer): ...
# class ProjectAlertSerializer(serializers.ModelSerializer): ... (with nested AlertType)

class ProjectSerializer(serializers.ModelSerializer):
    # Direct ForeignKey relationships (nested for full representation)
    us_state = UsStateSerializer(read_only=True)
    builder = BuilderSerializer(read_only=True)
    subscription_type = SubscriptionTypeSerializer(read_only=True)
    service_plan = ServicePlanSerializer(read_only=True)
    circuit = CircuitSerializer(read_only=True)
    network_type = ProjectNetworkTypeSerializer(read_only=True)

    # HasMany relationships (using SerializerMethodField for custom ordering/filtering)
    homes = serializers.SerializerMethodField()
    nodes = serializers.SerializerMethodField()
    node_frames = serializers.SerializerMethodField()
    uploads = serializers.SerializerMethodField()
    alerts = serializers.SerializerMethodField() # For ProjectAlerts

    class Meta:
        model = Project
        fields = '__all__'
        # You might explicitly list fields if you want to control the output
        # fields = [
        #     'project_id', 'circuit', 'name', 'address', 'city', 'us_state', 'zip_code',
        #     'longitude', 'latitude', 'builder', 'subscription_type', 'service_plan',
        #     'activation_date', 'active', 'domain_name', 'free_month', 'qbo_customer_id',
        #     'rm_property_id', 'created_at', 'updated_at',
        #     'homes', 'nodes', 'node_frames', 'uploads', 'alerts' # Include the nested fields here
        # ]

    # --- Methods for SerializerMethodField ---
    def get_homes(self, obj):
        # Equivalent of Laravel's `orderByRaw('CONVERT(unit, SIGNED)')`
        # This converts 'unit' to a numeric type for proper sorting.
        from .models.Home import Home
        from .serializers import HomeSerializer # Ensure HomeSerializer is defined
        qs = obj.homes.annotate(
            # Cast 'unit' CharField to Integer for sorting
            unit_as_int=Case(
                When(unit__regex=r'^\d+$', then=F('unit')), # Only cast if it's purely numeric
                default=Value(None), # Non-numeric units will be treated as None for sorting
                output_field=IntegerField()
            )
        ).order_by('unit_as_int', 'unit') # Sort by integer, then by original string for non-numeric

        return HomeSerializer(qs, many=True, read_only=True).data

    def get_nodes(self, obj):
        from .models.Node import Node
        from .serializers import NodeSerializer # Ensure NodeSerializer is defined
        return NodeSerializer(obj.nodes.all(), many=True, read_only=True).data

    def get_node_frames(self, obj):
        from .models.NodeFrame import NodeFrame
        from .serializers import NodeFrameSerializer # Ensure NodeFrameSerializer is defined
        return NodeFrameSerializer(obj.node_frames.all(), many=True, read_only=True).data

    def get_uploads(self, obj):
        from .models.Uploads import Uploads
        from .serializers import UploadsSerializer # Ensure UploadsSerializer is defined
        return UploadsSerializer(obj.uploads.all(), many=True, read_only=True).data

    def get_alerts(self, obj):
        # Equivalent of Laravel's `where("active", 1)->orderByDesc('alert_type_id')`
        from .models.ProjectAlert import ProjectAlert
        from .serializers import ProjectAlertSerializer # Ensure ProjectAlertSerializer is defined
        qs = obj.project_alerts.filter(active=True).order_by('-alert_type_id')
        return ProjectAlertSerializer(qs, many=True, read_only=True).data
    
class ProjectAlertSerializer(serializers.ModelSerializer):
    # Nested representation for AlertType
    # alert_type = serializers.PrimaryKeyRelatedField(read_only=True)  # Or AlertTypeSerializer if you want full details

    class Meta:
        model = ProjectAlert
        fields = '__all__'
        # You might explicitly list fields if you want to control the output
        # fields = ['id', 'project', 'alert_type', 'active', 'created_at', 'updated_at']    
        
class ProjectNetworkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectNetworkType
        fields = '__all__'
        # You might explicitly list fields if you want to control the output
        # fields = ['id', 'name', 'description', 'created_at', 'updated_at']        