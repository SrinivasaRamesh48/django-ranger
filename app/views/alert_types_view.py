from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.models.alert_type import AlertType
from app.serializers import AlertTypeSerializer

class AlertTypesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AlertType.objects.all()
    serializer_class = AlertTypeSerializer
    permission_classes = [IsAuthenticated]