from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from app.models.circuit_alert import CircuitAlert
from app.serializers.circuit_alert_serializer import CircuitAlertSerializer

class CircuitAlertViewSet(viewsets.ModelViewSet):
    queryset = CircuitAlert.objects.all()
    serializer_class = CircuitAlertSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'circuit_alert_id' 
    

    def perform_create(self, serializer):
        user = self.request.user
        is_active = serializer.validated_data.get('active', False)
        
        serializer.save(
            activated_by=user,
            updated_by=user,
            deactivated_by=user if not is_active else None
        )

    def perform_update(self, serializer):
        user = self.request.user
        instance = serializer.instance
        is_active = serializer.validated_data.get('active', instance.active)

        deactivated_by_user = instance.deactivated_by
        # If the alert was active and is now being deactivated, set the user.
        if instance.active and not is_active:
            deactivated_by_user = user
            
        serializer.save(
            updated_by=user,
            deactivated_by=deactivated_by_user
        )
    
    # Override create and update to provide a custom response format
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        response_data = {
            'success': True,
            'data': {"alert": serializer.data},
            'message': 'Circuit Alert Successfully Added.'
        }
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response_data = {
            'success': True,
            'data': True, # Matching Laravel's response of the update result
            'message': 'Circuit Alert Successfully Updated.'
        }
        return Response(response_data, status=status.HTTP_200_OK)