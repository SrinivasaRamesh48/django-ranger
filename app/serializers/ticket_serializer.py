from rest_framework import serializers
from app.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    entries = serializers.SerializerMethodField()
    ticket_category = serializers.StringRelatedField()
    ticket_status = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    subscriber = serializers.SerializerMethodField()

    minimize = serializers.SerializerMethodField()
    close_ticket = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = '__all__'

    def get_entries(self, obj):
        from app.serializers.ticket_entry_serializer import TicketEntrySerializer
        return TicketEntrySerializer(obj.entries.all(), many=True).data
        
    def get_subscriber(self, obj):
        from app.serializers.subscriber_serializer import SubscriberSerializer
        return SubscriberSerializer(obj.subscriber).data if obj.subscriber else None

    def get_minimize(self, obj):
        return False

    def get_close_ticket(self, obj):
        return False
