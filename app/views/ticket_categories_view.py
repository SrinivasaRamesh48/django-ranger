from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.serializers import TicketCategorySerializer
from app.models import TicketCategory

class TicketCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only ViewSet for retrieving Ticket Categories.
    - GET /ticket_categories -> Triggers the `list` action.
    """
    # The queryset defines the data to be returned.
    # The default ordering is already set in the model's Meta class.
    queryset = TicketCategory.objects.all()
    serializer_class = TicketCategorySerializer
    permission_classes = [IsAuthenticated]