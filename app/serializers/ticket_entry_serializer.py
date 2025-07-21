from rest_framework import serializers
from app.models import TicketEntry


class TicketEntrySerializer(serializers.ModelSerializer):
    dispatch_appointment = serializers.SerializerMethodField()
    # Nest a serializer to show user details instead of just the user ID.
    # user = UserSerializer(read_only=True) # Recommended approach
    user_info = serializers.CharField(source='user.username', read_only=True)

    # Nest a serializer for a one-to-many relationship
    actions = serializers.SerializerMethodField()

    # Use a SerializerMethodField to fetch and represent related data
    # that isn't a direct relationship on the model.
    latest_dispatch_appointment = serializers.SerializerMethodField()
    
    # Calculate the duration of the entry on the fly
    duration_minutes = serializers.SerializerMethodField()

    class Meta:
        model = TicketEntry
        fields = [
            'ticket_entry_id',
            'ticket',
            'user',
            'user_info', # More readable than just 'user' id
            'description',
            'notes_private',
            'start_time',
            'end_time',
            'duration_minutes',
            'submitted',
            'actions',
            'latest_dispatch_appointment',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'user': {'write_only': True},
            'ticket': {'required': False}  # Allow ticket to be set programmatically
        }

    def get_dispatch_appointment(self, obj):
        from app.serializers.dispatch_appointment_serializer import DispatchAppointmentSerializer
        return DispatchAppointmentSerializer(obj.dispatch_appointment).data if hasattr(obj, 'dispatch_appointment') and obj.dispatch_appointment else None

    def get_actions(self, obj):
        from app.serializers.ticket_entry_action_serializer import TicketEntryActionSerializer
        return TicketEntryActionSerializer(obj.actions.all(), many=True).data

    def get_latest_dispatch_appointment(self, obj):
        """
        Gets the most recent dispatch appointment associated with the entry's ticket.
        This mirrors the `dispatch_appointment` relationship in Laravel.
        """
        # Since the relationship may not exist, return None for now
        return None
        
    def get_duration_minutes(self, obj):
        """
        Calculates the difference between end_time and start_time in minutes.
        """
        if obj.end_time and obj.start_time:
            duration = obj.end_time - obj.start_time
            return int(duration.total_seconds() / 60)
        return 0
