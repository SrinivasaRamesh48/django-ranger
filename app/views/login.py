from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')  # for testing
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_data = {
            "user_id": 101,
            "email": "john.doe@example.com",
            "company": "TechCorp Inc.",
            "role": "Technician",
            "project_ids": [1, 2, 3],
            "permissions": ["view_tickets", "edit_profile", "access_dashboard"],
            "active_ticket": {
                "id": 555,
                "minimize": False,
                "close_ticket": False,
                # You can add more ticket fields here if needed
            },
            "alerts": [
                {"id": 1, "type": "High Priority"},
                {"id": 2, "type": "System Maintenance"}
            ],
            "sandbox": True
        }

        return Response({
            "success": True,
            "data": {
                "token": "fake123456tokenexample09876",
                "user": user_data
            },
            "message": "Login Successful"
        }, status=status.HTTP_200_OK)


class FakeAuthenticateView(APIView):
    permission_classes = [AllowAny]  # Optional: Allow all users to call this

    def get(self, request):
        fake_response = {
            'success': True,
            'data': {
                'token': 'FAKE123TOKEN456XYZ',
                'user': {
                    'id': 1,
                    'username': 'fake_user',
                    'email': 'fake@example.com',
                    'company': {
                        'id': 1,
                        'name': 'FakeCorp'
                    },
                    'role': {
                        'id': 1,
                        'name': 'Admin'
                    },
                    'project_ids': [101, 102],
                    'permission_identifiers': ['can_view_dashboard', 'can_edit_project'],
                    'alerts': [
                        {'type': 'info', 'message': 'This is a test alert.'}
                    ],
                    'sandbox': True,
                    'active_ticket': {
                        'id': 999,
                        'subject': 'Fake Ticket',
                        'status': 'Open',
                        'minimize': False,
                        'close_ticket': False
                    }
                }
            },
            'message': 'User Fake Authenticated.'
        }

        return Response(fake_response, status=200)


class FakeGetActiveTicketView(APIView):
    permission_classes = [AllowAny]  # Let anyone access this fake view

    def get(self, request):
        fake_ticket = {
            'id': 123,
            'subject': 'Fake Internet Issue',
            'status': 'Open',
            'opened_on': '2025-07-07T10:30:00Z',
            'ticket_status_id': 1,
            'ticket_category': {
                'id': 1,
                'name': 'Technical Support'
            },
            'user': {
                'id': 1,
                'username': 'fake_user'
            },
            'subscriber': {
                'id': 2,
                'name': 'John Doe',
                'home': {
                    'address': '123 Main St',
                    'mac_address': '00:11:22:33:44:55',
                    'node': 'Node-42',
                    'us_state': 'CA',
                    'project': 'Fiber Expansion'
                },
                'service_plan': {
                    'id': 1,
                    'description': 'Premium Plan',
                    'speed': '1 Gbps'
                }
            },
            'entries': [
                {
                    'id': 1,
                    'submitted': False,
                    'dispatch_appointment': {
                        'id': 10,
                        'technician': {'id': 5, 'name': 'Tech Joe'},
                        'type': {'id': 1, 'name': 'On-site'},
                        'timeslot': '2025-07-08T14:00:00Z',
                        'created_by': {'id': 1, 'name': 'Admin'},
                        'canceled_by': None
                    },
                    'actions': [
                        {'id': 1, 'type': {'id': 1, 'name': 'Inspection'}, 'notes': 'Checked modem'}
                    ],
                    'service_change_schedule': None
                }
            ],
            'minimize': False,
            'close_ticket': False
        }

        return Response({
            'success': 'true',
            'data': fake_ticket
        }, status=200)    