from rest_framework import serializers
from app.models import Ticket
from app.serializers.ticket_category_serializer import TicketCategorySerializer
from app.serializers.user_serializer import UserSerializer
from app.serializers.ticket_status_serializer import TicketStatusSerializer
from app.serializers.ticket_entry_serializer import TicketEntrySerializer

class TicketSerializer(serializers.ModelSerializer):
    ticket_category = TicketCategorySerializer(read_only=True)
    user = UserSerializer(read_only=True)
    ticket_status = TicketStatusSerializer(read_only=True)
    entries = TicketEntrySerializer(many=True, read_only=True)
    class Meta:
        model = Ticket
        fields = [
            'ticket_id',
            'opened_on',
            'reopened_on',
            'closed_on',
            'created_at',
            'updated_at',
            'subscriber',
            'user',
            'ticket_category',
            'ticket_status',
            'entries',
            'minimize',
            'close_ticket'
        ]
