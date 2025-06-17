from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.models.AlertType import AlertType
from app.serializers import AlertTypeSerializer

class AlertTypesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only ViewSet for retrieving alert types.
    This corresponds to `AlertTypesController@index`.
    It handles the GET request for the list of alert types.
    
    - GET /alert_types/ -> Triggers the `list` action.
    """
    # The queryset defines the data to be returned.
    # The default ordering is already set in the model's Meta class.
    queryset = AlertType.objects.all()
    
    # The serializer class to use for converting the queryset objects.
    serializer_class = AlertTypeSerializer
    
    # Protects the endpoint, requiring authentication.
    permission_classes = [IsAuthenticated]