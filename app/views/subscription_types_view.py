from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.serializers.subscription_type_serializer import SubscriptionTypeSerializer
from app.models import SubscriptionType



class SubscriptionTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubscriptionType.objects.all()
    serializer_class = SubscriptionTypeSerializer
    permission_classes = [IsAuthenticated]