
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.models.interest_form_log import InterestFormLog
from app.serializers.interest_form_log_serializer import InterestFormLogSerializer

class InterestFormLogViewSet(viewsets.ModelViewSet):
    queryset = InterestFormLog.objects.select_related('us_state', 'updated_by').all()
    
    serializer_class = InterestFormLogSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'interest_form_log_id' 
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Logs Successfully Retrieved.'
        })

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'success': True,
            'data': True, # Matching Laravel's response
            'message': 'Log Successfully Updated.'
        })