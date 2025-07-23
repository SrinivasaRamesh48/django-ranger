from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.serializers.us_state_serializer import UsStateSerializer
from app.models import UsState

class UsStateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UsState.objects.all()
    serializer_class = UsStateSerializer
    permission_classes = [IsAuthenticated]