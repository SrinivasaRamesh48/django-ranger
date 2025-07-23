from rest_framework import serializers
from app.models import TicketCategory


class TicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCategory
        fields = ['ticket_category_id', 'description','account_portal_visible']
