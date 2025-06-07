from rest_framework import serializers
from app.models.Ticket import Ticket
from app.models.TicketCategory import TicketCategory
from app.models.TicketEntry import TicketEntry
from app.models.TicketEntryAction import TicketEntryAction
from app.models.TicketEntryActionType import TicketEntryActionType
from app.models.TicketStatus import TicketStatus


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class TicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCategory
        fields = '__all__' # This will include all fields from the model

class TicketEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketEntry
        fields = '__all__'
        # Or explicitly list them:
        # fields = ['ticket_category_id', 'description', 'created_at', 'updated_at']
        
class TicketEntryActionSerializer(serializers.ModelSerializer):
    # Optional: For nested representations
    # ticket_entry = TicketEntrySerializer(read_only=True)
    # ticket_entry_action_type = TicketEntryActionTypeSerializer(read_only=True)

    class Meta:
        model = TicketEntryAction
        fields = '__all__' # This will include all fields from the model
        # Or explicitly list them:
        
class TicketEntryActionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketEntryActionType
        fields = '__all__' # This will include all fields from the model
        # Or explicitly list them:
        # fields = ['name', 'description', 'created_at', 'updated_at']

class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatus
        fields = '__all__' # This will include all fields from the model
        # Or explicitly list them:
        # fields = ['name', 'description', 'created_at', 'updated_at']