from rest_framework import serializers
from app.models import ServiceChangeSchedule, Subscriber, ServicePlan, Ticket, ServiceChangeScheduleType, LeasingStaffRed
from app.serializers.service_plan_serializer import ServicePlanSerializer
from app.serializers.service_change_schedule_type_serializer import ServiceChangeScheduleTypeSerializer
from app.serializers.leasing_staff_red_serializer import LeasingStaffRedSerializer
from app.serializers.ticket_serializer import TicketSerializer
from app.serializers.subscriber_serializer import SubscriberSerializer

class ServiceChangeScheduleSerializer(serializers.ModelSerializer):
    subscriber = SubscriberSerializer(read_only=True)
    service_plan = ServicePlanSerializer(read_only=True)
    ticket_entry = TicketSerializer(read_only=True)
    type = ServiceChangeScheduleTypeSerializer(read_only=True)
    leasing_staff_red = LeasingStaffRedSerializer(read_only=True)

    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)
    service_plan_id = serializers.PrimaryKeyRelatedField(queryset=ServicePlan.objects.all(), source='service_plan', write_only=True)
    ticket_entry_id = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all(), source='ticket_entry', write_only=True, required=False, allow_null=True)
    service_change_schedule_type_id = serializers.PrimaryKeyRelatedField(queryset=ServiceChangeScheduleType.objects.all(), source='type', write_only=True)
    leasing_staff_red_id = serializers.PrimaryKeyRelatedField(queryset=LeasingStaffRed.objects.all(), source='leasing_staff_red', write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ServiceChangeSchedule
        fields = '__all__'
