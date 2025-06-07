# app/serializers.py

from rest_framework import serializers
from app.models.ServiceChangeSchedule import ServiceChangeSchedule # Import the model
 # Import the model
from app.models.ServicePlan import ServicePlan 
from app.models.ServiceChangeScheduleType import ServiceChangeScheduleType
# Optional: If you want nested representations of related objects:
# from .serializers import ServiceChangeScheduleTypeSerializer, SubscriberSerializer, ServicePlanSerializer, TicketSerializer, LeasingStaffRedSerializer

# ... (your other serializers) ...

class ServiceChangeScheduleSerializer(serializers.ModelSerializer):
    # Optional: For nested representations
    # service_change_schedule_type = ServiceChangeScheduleTypeSerializer(read_only=True)
    # subscriber = SubscriberSerializer(read_only=True)
    # service_plan = ServicePlanSerializer(read_only=True)
    # ticket_entry = TicketSerializer(read_only=True)
    # leasing_staff_red = LeasingStaffRedSerializer(read_only=True)

    class Meta:
        model = ServiceChangeSchedule
        fields = '__all__'
        # For sensitive fields like passkeys, consider making them write_only or excluding them from read.
        # extra_kwargs = {
        #     'passkey_1': {'write_only': True},
        #     'passkey_2': {'write_only': True},
        # }
        # Or specify explicit fields:
        # fields = [
        #     'service_change_schedule_id', 'service_change_schedule_type', 'subscriber',
        #     'service_plan', 'ticket_entry', 'ssid_1', 'passkey_1', 'ssid_2', 'passkey_2',
        #     'leasing_staff_red', 'process_on', 'processed', 'canceled',
        #     'created_at', 'updated_at'
        # ]
        
class ServiceChangeScheduleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceChangeScheduleType
        fields = '__all__'
        # If you want to exclude certain fields, you can do so:
        # exclude = ['created_at', 'updated_at']
        # Or specify explicit fields:
        # fields = ['service_change_schedule_type_id', 'description', 'created_at', 'updated_at']        
class ServicePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePlan
        fields = '__all__'
        # If you want to exclude certain fields, you can do so:
        # exclude = ['created_at', 'updated_at']
        # Or specify explicit fields:
        # fields = ['service_plan_id', 'name', 'description', 'created_at', 'updated_at']        