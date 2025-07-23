from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.models.circuit_carrier import CircuitCarrier
from app.serializers.circuit_carrier_serializer import CircuitCarrierSerializer

class CircuitCarrierViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CircuitCarrier.objects.all()
    serializer_class = CircuitCarrierSerializer
    permission_classes = [IsAuthenticated]
