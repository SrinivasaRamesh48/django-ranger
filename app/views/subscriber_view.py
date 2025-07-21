from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch

from app.models import Subscriber, MultiHomeSubscriberHome
from app.serializers.subscriber_serializer import SubscriberSerializer

class SubscriberListView(APIView):
    def get(self, request):
        subscribers = Subscriber.objects.select_related(
            'service_plan',
            'home__us_state',
            'home__project__subscription_type',
            'home__node',
        ).prefetch_related(
            'home__mac_address'
        ).order_by('-subscriber_id')

        # Add multi_homes attribute dynamically
        subscriber_list = []
        for subscriber in subscribers:
            if subscriber.multi_home_subscriber:
                multi_homes = MultiHomeSubscriberHome.objects.select_related(
                    'home__mac_address'
                ).filter(subscriber_id=subscriber.subscriber_id)
                subscriber.multi_homes_data = multi_homes
            else:
                subscriber.multi_homes_data = None

            subscriber_list.append(subscriber)

        serializer = SubscriberSerializer(subscriber_list, many=True)

        return Response({
            'success': bool(subscriber_list),
            'data': serializer.data,
            'message': 'Subscribers Successfully Retrieved.' if subscriber_list else 'Failed to Retrieve Subscribers.'
        }, status=status.HTTP_200_OK)
