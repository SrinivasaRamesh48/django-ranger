from rest_framework import serializers
from app.models import TicketEntry
from app.serializers.ticket_entry_action_serializer import TicketEntryActionSerializer
from app.serializers.dispatch_appointment_serializer import DispatchAppointmentSerializer
from app.models import DispatchAppointment

class TicketEntrySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    actions = TicketEntryActionSerializer(many=True, read_only=True, source='ticketentryaction_set')
    latest_dispatch_appointment = serializers.SerializerMethodField()
    dispatch_appointment = serializers.SerializerMethodField()
    duration_minutes = serializers.SerializerMethodField()

    class Meta:
        model = TicketEntry
        fields = [
            'ticket_entry_id',
            'description',
            'notes_private',
            'start_time',
            'end_time',
            'duration_minutes',
            'username',
            'actions',
            'dispatch_appointment',
            'latest_dispatch_appointment',
            # Add other fields you want explicitly
        ]

    def get_dispatch_appointment(self, obj):
        appointment = getattr(obj, 'dispatch_appointment', None)
        if appointment:
            return DispatchAppointmentSerializer(appointment).data
        return None

    def get_latest_dispatch_appointment(self, obj):
        latest = DispatchAppointment.objects.filter(ticket_entry=obj).order_by('-date').first()
        if latest:
            return DispatchAppointmentSerializer(latest).data
        return None

    def get_duration_minutes(self, obj):
        if obj.start_time and obj.end_time:
            delta = obj.end_time - obj.start_time
            return int(delta.total_seconds() // 60)
        return None

