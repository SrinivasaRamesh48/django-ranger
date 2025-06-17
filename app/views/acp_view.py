from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from app.models.Subscriber import Subscriber 
from app.serializers import SubscriberSerializer 


class SubscriberACPViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and managing ACP enrollments for Subscribers.
    This replaces the separate function-based views.
    """
    serializer_class = SubscriberSerializer
    permission_classes = [AllowAny]
    
    # Set the lookup field to match the URL parameter name `id` if you prefer it over `pk`
    lookup_field = 'pk'
    
    # The base queryset for the ViewSet
    queryset = Subscriber.objects.all().select_related(
        'service_plan', 'home__us_state', 'home__project'
    )

    def get_queryset(self):
        """
        Overrides the default queryset to only list subscribers
        with an ACP Application ID, matching the original `index` logic.
        This affects the `list` action.
        """
        # This is called for the 'list' view (e.g., GET /allACP)
        return self.queryset.filter(acp_application_id__isnull=False)

    @action(detail=False, methods=['post'], url_path='enroll')
    def enroll(self, request):
        """
        Corresponds to the `acp_enroll` function.
        Updates a subscriber with a new ACP Application ID.
        Accessed via POST /acp_enroll
        """
        subscriber_id = request.data.get('subscriber_id')
        acp_application_id = request.data.get('acp_application_id')

        if not all([subscriber_id, acp_application_id]):
            return Response({
                'success': False, 
                'message': 'subscriber_id and acp_application_id are required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            subscriber = Subscriber.objects.get(subscriber_id=subscriber_id)
            subscriber.acp_application_id = acp_application_id
            subscriber.save(update_fields=['acp_application_id'])
            return Response({
                'success': True,
                'message': 'Enrollment Successful.'
            }, status=status.HTTP_200_OK)
        except Subscriber.DoesNotExist:
            return Response({'success': False, 'message': 'Subscriber not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'success': False, 'message': 'Failed to Enroll.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='cancel-enrollment')
    def cancel_enrollment(self, request, pk=None):
        """
        Corresponds to `cancel_acp_enrollment`.
        Sets the acp_application_id to NULL. The `pk` is the subscriber_id.
        Accessed via PUT /cancel_acp_enrollment/{id}
        """
        try:
            subscriber = self.get_object() # Retrieves the subscriber using the pk from the URL
            subscriber.acp_application_id = None
            subscriber.save(update_fields=['acp_application_id'])
            return Response({
                'success': True,
                'message': 'Enrollment Successfully Canceled.'
            }, status=status.HTTP_200_OK)
        except Exception:
            # The get_object() method will raise a 404 if not found automatically.
            return Response({
                'success': False,
                'message': 'Failed to Cancel Enrollment.'
            }, status=status.HTTP_400_BAD_REQUEST)