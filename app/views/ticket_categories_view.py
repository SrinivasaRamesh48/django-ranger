from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.serializers.ticket_category_serializer import TicketCategorySerializer
from app.models import TicketCategory


class TicketCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TicketCategory.objects.all()
    serializer_class = TicketCategorySerializer
    permission_classes = [IsAuthenticated]