# app/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch

# Import models and the main serializer
from app.models import Subscriber, Home, MacAddress,UsState, Project, ServicePlan, Node,MultiHomeSubscriberHome
from app.serializers import SubscriberSerializer

class SubscriberListView(APIView):
    """
    Handles fetching a list of all subscribers with their detailed, nested data.
    Equivalent to the SubscriberController@index method.
    """
    def get(self, request):
        """
        Retrieves a list of all subscribers, ordered by the most recent.
        """
        try:
            subscribers = Subscriber.objects.prefetch_related(
        
                Prefetch('service_plan', queryset=ServicePlan.objects.only(
                    'service_plan_id', 'description', 'amount', 'bulk', 'active'
                )),
                Prefetch('home', queryset=Home.objects.select_related(
                    'us_state', 'project__subscription_type', 'project__network_type', 'node'
                ).prefetch_related('mac_address').only(
                    'home_id', 'address', 'unit', 'state_id', 'city', 'zip_code',
                    'node_switch_unit', 'node_switch_module', 'node_port_num',
                    'project_id', 'mac_address_id', 'node_id',
                    # Include fields needed for related objects
                    'us_state__state_id', 'us_state__abbr', 'us_state__name',
                    'project__project_id', 'project__name', 'project__subscription_type_id',
                    'project__project_network_type_id',
                    'project__subscription_type__subscription_type_id',
                    'project__subscription_type__name',
                    'project__network_type__project_network_type_id',
                    'project__network_type__description',
                    'node__node_id', 'node__hostname',
                    'mac_address__mac_address_id', 'mac_address__home_id',
                    'mac_address__address', 'mac_address__cpe_serial_number'
                )),
                # Prefetch multi-home data for subscribers who have it
                Prefetch('multi_homes', queryset=MultiHomeSubscriberHome.objects.select_related(
                    'home__mac_address'
                ))
            ).order_by("-subscriber_id")

            # The serializer handles the final JSON structure, including the logic
            # for multi_homes which was previously in the foreach loop.
            serializer = SubscriberSerializer(subscribers, many=True)

            response = {
                'success': True,
                'data': serializer.data,
                'message': 'Subscribers Successfully Retrieved.'
            }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            # Professional error handling
            response = {
                'success': False,
                'data': None,
                'message': f'Failed to Retrieve Subscribers: {str(e)}'
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

