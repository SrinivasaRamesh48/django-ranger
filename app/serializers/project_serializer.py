from rest_framework import serializers
from app.models import Project, UsState, Builder, SubscriptionType, ServicePlan, Circuit
from app.serializers.us_state_serializer import UsStateSerializer
from app.serializers.builder_serializer import BuilderSerializer
from app.serializers.subscription_type_serializer import SubscriptionTypeSerializer
from app.serializers.service_plan_serializer import ServicePlanSerializer
from app.serializers.circuit_serializer import CircuitSerializer


class ProjectSerializer(serializers.ModelSerializer):
    us_state = UsStateSerializer(read_only=True)
    builder = BuilderSerializer(read_only=True)
    subscription_type = SubscriptionTypeSerializer(read_only=True)
    service_plan = ServicePlanSerializer(read_only=True)
    circuit = CircuitSerializer(read_only=True)

    state_id = serializers.PrimaryKeyRelatedField(queryset=UsState.objects.all(), source='us_state', write_only=True)
    builder_id = serializers.PrimaryKeyRelatedField(queryset=Builder.objects.all(), source='builder', write_only=True, required=False, allow_null=True)
    subscription_type_id = serializers.PrimaryKeyRelatedField(queryset=SubscriptionType.objects.all(), source='subscription_type', write_only=True)
    bulk_service_plan_id = serializers.PrimaryKeyRelatedField(queryset=ServicePlan.objects.all(), source='service_plan', write_only=True, required=False, allow_null=True)
    circuit_id = serializers.PrimaryKeyRelatedField(queryset=Circuit.objects.all(), source='circuit', write_only=True, required=False, allow_null=True)

    class Meta:
        model = Project
        fields = [
            'project_id', 'name', 'address', 'city', 'zip_code', 'longitude', 'latitude', 
            'activation_date', 'active', 'domain_name', 'free_month', 'qbo_customer_id', 
            'rm_property_id',
            'us_state', 'builder', 'subscription_type', 'service_plan', 'circuit',
            'state_id', 'builder_id', 'subscription_type_id', 'bulk_service_plan_id', 'circuit_id'
        ]
        read_only_fields = ['created_at', 'updated_at']
