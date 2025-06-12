from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.models.Alert import Alert
from app.serializers.AlertTypeSerializer import AlertSerializer

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
        """
        Custom logic to run when a new alert is created (replaces store()).
        """
        user = self.request.user
        # The 'active' status is in the validated data from the request
        is_active = serializer.validated_data.get('active', False)
        
        # This is where we inject the user IDs, similar to the Laravel controller
        serializer.save(
            activated_by=user,
            updated_by=user,
            deactivated_by=user if not is_active else None
        )

    def perform_update(self, serializer):
        """
        Custom logic to run when an existing alert is updated (replaces update()).
        """
        user = self.request.user
        # Get the instance being updated to check its original 'active' state
        instance = serializer.instance 
        # Get the new 'active' state from the request data
        is_active = serializer.validated_data.get('active', instance.active)
        
        # Determine the 'deactivated_by' field based on the NEW active state
        deactivated_by = None
        if instance.active and not is_active:
            # The alert was active and is now being deactivated
            deactivated_by = user
        elif not instance.active and not is_active:
            # If it was already inactive, preserve who deactivated it originally
            deactivated_by = instance.deactivated_by
            
        serializer.save(
            updated_by=user,
            deactivated_by=deactivated_by
        )