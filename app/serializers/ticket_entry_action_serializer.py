from rest_framework import serializers
from app.models import TicketEntryAction, TicketEntryActionType
from app.serializers.ticket_entry_action_type_serializer import TicketEntryActionTypeSerializer


class TicketEntryActionSerializer(serializers.ModelSerializer):
    type = TicketEntryActionTypeSerializer(read_only=True)
    ticket_entry_action_type_id = serializers.PrimaryKeyRelatedField(queryset=TicketEntryActionType.objects.all(), source='type', write_only=True)

    class Meta:
        model = TicketEntryAction
        fields = [
            'ticket_entry_action_id',
            'type', 'ticket_entry_action_type_id'
        ]
