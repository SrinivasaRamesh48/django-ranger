from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.serializers.us_state_serializer import UsStateSerializer
from app.models import UsState
# from .models import UsState
# from .serializers import UsStateSerializer

class UsStateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only ViewSet for retrieving US States.
    - GET /us_states -> Triggers the `list` action.
    """
    # The queryset defines the data to be returned.
    # The default ordering is already set in the model's Meta class.
    queryset = UsState.objects.all()
    serializer_class = UsStateSerializer
    permission_classes = [IsAuthenticated]