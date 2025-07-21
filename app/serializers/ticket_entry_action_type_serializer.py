from rest_framework import serializers
from app.models import TicketEntryActionType


class TicketEntryActionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketEntryActionType
        fields = ['ticket_entry_action_type_id', 'description']
