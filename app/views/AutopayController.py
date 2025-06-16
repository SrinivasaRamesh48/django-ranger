from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app.models.Subscriber import Subscriber
from app.Serializers import SubscriberSerializer

class AutopayViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only ViewSet for listing subscribers with autopay enabled.
    This corresponds to `AutopayController@index`.
    """
    serializer_class = SubscriberSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Defines the data for the view. Corresponds to the Eloquent query:
        Subscriber::with([...])->whereNotNull("autopay_merchant_id")->orderByDesc(...)
        """
        return Subscriber.objects.filter(autopay_merchant_id__isnull=False) \
                                 .select_related('service_plan', 'home__us_state', 'home__project')

    def list(self, request, *args, **kwargs):
        """
        Overrides the default list action to provide a custom response format
        that matches the original Laravel API.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        
        response_data = {
            'success': True if data else False,
            'data': data,
            'message': 'Subscribers Successfully Retrieved.' if data else 'Failed to Retrieve Subscribers.'
        }
        
        return Response(response_data, status=status.HTTP_200_OK)