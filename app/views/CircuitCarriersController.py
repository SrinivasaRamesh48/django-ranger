from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.models.CircuitCarrier import CircuitCarrier
from app.Serializers import CircuitCarrierSerializer

class CircuitCarrierViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only ViewSet for retrieving circuit carriers.
    This corresponds to `CircuitCarriersController@index`.
    - GET /circuit_carriers -> Triggers the `list` action.
    """
    # The queryset defines the data to be returned.
    # The default ordering is already set in the model's Meta class.
    queryset = CircuitCarrier.objects.all()
    serializer_class = CircuitCarrierSerializer
    permission_classes = [IsAuthenticated]
