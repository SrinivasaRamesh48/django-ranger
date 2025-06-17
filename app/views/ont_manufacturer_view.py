from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.models import OntManufacturer
from app.serializers import OntManufacturerSerializer

class OntManufacturerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only ViewSet for retrieving ONT Manufacturers.
    This corresponds to `OntManufacturerController@index`.
    - GET /ont_manufacturers -> Triggers the `list` action.
    """
    # The queryset defines the data to be returned.
    # The default ordering is already set in the model's Meta class.
    queryset = OntManufacturer.objects.all()
    serializer_class = OntManufacturerSerializer
    permission_classes = [IsAuthenticated]