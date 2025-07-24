from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.models import OntManufacturer
from app.serializers.ont_manufacturer_serializer import OntManufacturerSerializer

class OntManufacturerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OntManufacturer.objects.all()
    serializer_class = OntManufacturerSerializer
    permission_classes = [IsAuthenticated]