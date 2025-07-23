from rest_framework import serializers
from app.models import DispatchAppointment, DispatchAppointmentType, User, DispatchAppointmentTimeslot, Ticket
from app.serializers.dispatch_appointment_type_serializer import DispatchAppointmentTypeSerializer
from app.serializers.user_serializer import UserSerializer
from app.serializers.dispatch_appointment_timeslot_serializer import DispatchAppointmentTimeslotSerializer
from app.serializers.ticket_serializer import TicketSerializer

class DispatchAppointmentSerializer(serializers.ModelSerializer):
    appointment_type = DispatchAppointmentTypeSerializer(read_only=True)
    technician = UserSerializer(read_only=True)
    timeslot = DispatchAppointmentTimeslotSerializer(read_only=True)
    ticket = TicketSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    canceled_by = UserSerializer(read_only=True)
    dispatch_appointment_type_id = serializers.PrimaryKeyRelatedField(queryset=DispatchAppointmentType.objects.all(), source='appointment_type', write_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='technician', write_only=True)
    dispatch_appointment_timeslot_id = serializers.PrimaryKeyRelatedField(queryset=DispatchAppointmentTimeslot.objects.all(), source='timeslot', write_only=True)
    ticket_id = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all(), source='ticket', write_only=True, required=False, allow_null=True)
    created_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='created_by', write_only=True)
    canceled_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='canceled_by', write_only=True, required=False, allow_null=True)
    
    
    
    class Meta:
        model = DispatchAppointment
        fields = ['dispatch_appointment_id', 'date', 'appointment_type', 'technician', 'timeslot', 'ticket', 'created_by', 'canceled_by', 'dispatch_appointment_type_id', 'user_id', 'dispatch_appointment_timeslot_id', 'ticket_id', 'created_by_id', 'canceled_by_id']
