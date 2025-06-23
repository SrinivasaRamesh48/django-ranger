from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app import models
from app.models import Payment
from app.serializers import PaymentSerializer 


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only ViewSet for viewing Payments.
    """
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'payment_id'

    def get_serializer_class(self):
        return PaymentSerializer

    def list(self, request, *args, **kwargs):
        """
        Corresponds to the `index` method.
        Eager loads related data for efficiency.
        """
        queryset = self.get_queryset().select_related(
            'subscriber__service_plan',
            'subscriber__home__us_state',
            'subscriber__home__project'
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Payments Successfully Retrieved.'
        })

    def retrieve(self, request, *args, **kwargs):
        """
        Corresponds to the `show` method.
        Uses prefetch_related for deeply nested data.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Payment Successfully Retrieved.'
        })

    def get_object(self):
        """
        Override get_object to add prefetching for the detail view.
        """
        obj = super().get_object()
        if self.action == 'retrieve':
            # This is the Django equivalent of the deep `with()` call
            models.prefetch_related_objects([obj],
                'subscriber__service_plan',
                'subscriber__home__us_state',
                'subscriber__home__project',
                'statement__items__description__type',
                'statement__items__payment'
            )
        return obj