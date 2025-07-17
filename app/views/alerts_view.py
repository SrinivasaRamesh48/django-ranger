from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.models.alert import Alert
from app.serializers import AlertSerializer

class AlertViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for creating, retrieving, and updating alerts.
    - GET /alerts/ -> list() -> index()
    - POST /alerts/ -> create() -> store()
    - PUT /alerts/{id}/ -> update() -> update()
    - PATCH /alerts/{id}/ -> partial_update() -> update()
    - GET /alerts/{id}/ -> retrieve()
    """
    queryset = Alert.objects.all().select_related(
        'alert_type', 'activated_by', 'deactivated_by', 'updated_by'
    )
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'alert_id' # To use 'alert_id' in the URL instead of 'pk'

    def perform_create(self, serializer):
        # Custom logic to run when a new alert is created.
        user = self.request.user
        is_active = serializer.validated_data.get('active', False)
        serializer.save(
            activated_by=user,
            updated_by=user,
            deactivated_by=user if not is_active else None
        )

    def perform_update(self, serializer):
        # Custom logic to run when an existing alert is updated.
        user = self.request.user
        instance = serializer.instance 
        is_active = serializer.validated_data.get('active', instance.active)
        deactivated_by = None
        if instance.active and not is_active:
            deactivated_by = user
        elif not instance.active and not is_active:
            deactivated_by = instance.deactivated_by
            
        serializer.save(
            updated_by=user,
            deactivated_by=deactivated_by
        )