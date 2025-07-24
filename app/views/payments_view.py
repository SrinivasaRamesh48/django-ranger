from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app import models
from app.models import Payment
from app.serializers.payment_serializer import PaymentSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'payment_id'

    def get_serializer_class(self):
        return PaymentSerializer
    
    def list(self, request, *args, **kwargs):
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
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Payment Successfully Retrieved.'
        })

    def get_object(self):
        obj = super().get_object()
        if self.action == 'retrieve':
            models.prefetch_related_objects([obj],
                'subscriber__service_plan',
                'subscriber__home__us_state',
                'subscriber__home__project',
                'statement__items__description__type',
                'statement__items__payment'
            )
        return obj