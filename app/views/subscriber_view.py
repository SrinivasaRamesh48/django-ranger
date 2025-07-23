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


class CheckOpenTicketsView(APIView):
    def get(self, request, id):
        try:
            subscriber = Subscriber.objects.get(pk=id)
        except Subscriber.DoesNotExist:
            return Response({"error": "Subscriber not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = {
    'subscriber_id': 6,
    'first_name': 'Test',
    'last_name': 'User',
    'primary_email': 'test@gmail.com',
    'username': 'testuser123',
    'primary_phone': '123-456-7890',
    'service_activated_on': '2024-06-01T10:00:00Z',
    'service_deactivated_on': None,
    'suspended': False,
    'merchant_customer_id': 'MCID_948302',
    'autopay_merchant_id': 'AP_2938483',
    'acp_application_id': 'ACP_0048',
    'qbo_customer_id': 'QBO_9900123',
    'multi_home_subscriber': True,
    'pause_billing': False,
    'created_at': '2025-07-21T06:25:08.749162Z',
    'updated_at': '2025-07-22T06:25:08.749376Z',

    'home': {
        'id': 10,
        'name': 'Test Residence',
        'address': '123 Main Street',
        'city': 'Springfield',
        'zipcode': '54321'
    },
    'service_plan': {
        'id': 2,
        'name': 'Fiber Max 500',
        'download_speed': '500 Mbps',
        'upload_speed': '500 Mbps',
        'price': '79.99'
    },
    'node': {
        'id': 3,
        'name': 'Node Alpha',
        'location': 'North Region'
    },

    'tickets': [
        {
            'id': 1,
            'ticket_category': 'Billing',
            'status': 'Closed',
            'entries': [
                {'id': 1, 'content': 'Customer inquired about invoice #123.'},
                {'id': 2, 'content': 'Explained charges and resolved issue.'}
            ]
        },
        {
            'id': 2,
            'ticket_category': 'Technical',
            'status': 'Open',
            'entries': [
                {'id': 3, 'content': 'Internet outage reported.'},
                {'id': 4, 'content': 'Technician scheduled for 2 PM visit.'}
            ]
        }
    ],

    'open_tickets': [
        {
            'id': 2,
            'ticket_category': 'Technical',
            'entries': [
                {'id': 3, 'content': 'Internet outage reported.'},
                {'id': 4, 'content': 'Technician scheduled for 2 PM visit.'}
            ]
        }
    ],

    'statement': {
        'id': 15,
        'period_start': '2025-07-01',
        'period_end': '2025-07-31',
        'amount_due': '79.99',
        'due_date': '2025-08-05'
    },

    'statements': [
        {
            'id': 14,
            'period_start': '2025-06-01',
            'period_end': '2025-06-30',
            'amount_due': '79.99',
            'due_date': '2025-07-05',
            'paid': True
        },
        {
            'id': 15,
            'period_start': '2025-07-01',
            'period_end': '2025-07-31',
            'amount_due': '79.99',
            'due_date': '2025-08-05',
            'paid': False
        }
    ],

    'payments': [
        {
            'id': 101,
            'amount': '79.99',
            'date': '2025-07-05',
            'method': 'Credit Card'
        },
        {
            'id': 102,
            'amount': '79.99',
            'date': '2025-06-05',
            'method': 'ACH'
        }
    ],

    'payment_methods': [
        {
            'id': 501,
            'type': 'Credit Card',
            'last4': '4242',
            'exp_date': '12/26'
        },
        {
            'id': 502,
            'type': 'ACH',
            'bank_name': 'Chase Bank'
        }
    ],

    'multi_homes': [
        {
            'id': 201,
            'name': 'Vacation Home',
            'address': '456 Lakeview Road',
            'city': 'Laketown',
            'zipcode': '65432'
        }
    ],

    'alerts': [
        {
            'id': 301,
            'type': 'Outage',
            'message': 'Scheduled maintenance on 2025-07-25 between 1 AM and 3 AM.',
            'severity': 'Info'
        },
        {
            'id': 302,
            'type': 'Billing',
            'message': 'Payment overdue for July statement.',
            'severity': 'Warning'
        }
    ]
}

        
        return Response(serializer)