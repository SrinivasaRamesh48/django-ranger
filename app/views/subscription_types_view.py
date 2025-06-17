from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.serializers import SubscriptionTypeSerializer
from app.models import SubscriptionType



class SubscriptionTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only ViewSet for retrieving Subscription Types.
    - GET /subscription_types -> Triggers the `list` action.
    """
    queryset = SubscriptionType.objects.all()
    serializer_class = SubscriptionTypeSerializer
    permission_classes = [IsAuthenticated]