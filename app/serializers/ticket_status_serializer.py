from rest_framework import serializers
from app.models import TicketStatus


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatus
        fields = ['ticket_status_id', 'description']
