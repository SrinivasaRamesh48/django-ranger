import string
import random
from django.contrib.auth.hashers import make_password
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from oauth2_provider.models import get_access_token_model
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from app.models import (User, Project, UserPermissionDefaults, UserProjects, UserPermissions)
from app.mail.technician_welcome import send_technician_welcome_email
# technical_password_update
from app.mail.technician_password_updated import send_technician_password_updated_email  
from oauth2_provider.models import Application
from oauthlib.common import generate_token
from oauth2_provider.models import AccessToken, RefreshToken
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny,IsAuthenticated
from app.models import UserProjects, UserPermissions, Ticket, Alert
from app.serializers import UserSerializer, PasswordResetSerializer
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.hashers import check_password

def generate_random_password(length=16):
    """Generates a random password, equivalent to your PHP logic."""
    pool = string.ascii_letters + string.digits
    return ''.join(random.choice(pool) for i in range(length))

class RegisterView(generics.CreateAPIView):
    """
    Endpoint for user registration.
    Corresponds to your `register` method.
    Protected by scope, so only an authenticated user (like an admin) can create another user.
    """
    queryset = User.objects.all()
    # serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope] # Protects the endpoint

    def perform_create(self, serializer):
        # Generate a temporary password
        random_password = generate_random_password()
        
        # Create the user instance but don't save it yet
        user = serializer.save(
            password=make_password(random_password),
            username=serializer.validated_data['email'] # Use email as username for simplicity
        )

        # Assign default permissions based on role
        if user.role:
            default_permissions = UserPermissionDefaults.objects.filter(role=user.role)
            for perm in default_permissions:
                UserPermissions.objects.create(user=user, permission_type=perm.permission_type)

        # Assign all projects to the new user
        all_projects = Project.objects.all()
        for project in all_projects:
            UserProjects.objects.create(user=user, project=project)

        # Send welcome email using your custom mailer
        # Assumes `send_technician_welcome_email` function takes the user object and the password
        send_technician_welcome_email(user, random_password)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(username=email, password=password)
        print(f"Authenticating user: {user}")
        if user and user.active:
            app = Application.objects.get(name='Frontend App')  # or use filter with client_id
            expires = timezone.now() + timedelta(seconds=36000)
            access_token = AccessToken.objects.create(
                user=user,
                application=app,
                expires=expires,
                token=generate_token(),
                scope='read write'
            )
            refresh_token = RefreshToken.objects.create(
                user=user,
                token=generate_token(),
                access_token=access_token,
                application=app
            )

            return Response({
                'success': True,
                'data': {
                    'token': access_token.token,
                    'refresh_token': refresh_token.token,
                    'user': UserSerializer(user).data
                },
                'message': 'Login Successful'
            }, status=200)
        else:
            return Response({'success': False, 'message': 'Invalid credentials'}, status=400)


User = get_user_model()

class AuthenticateView(APIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        print(f"Authenticating user: {user}")
        if not user.is_active:
            return Response({'success': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user.company = getattr(user, 'company', None)
        user.role = getattr(user, 'role', None)

        user.projects = UserProjects.objects.filter(user_id=user.user_id)
        user.project_ids = [p.project_id for p in user.projects]

        user.permissions = UserPermissions.objects.select_related("user_permission_type").filter(user_id=user.user_id)
        user.permission_identifiers = [perm.user_permission_type.identifier for perm in user.permissions if perm.user_permission_type]

        active_ticket = Ticket.objects.filter(
            entries__submitted=False,
            entries__user_id=user.user_id
        ).prefetch_related(
            'entries',
            'entries__dispatch_appointment',
            'entries__dispatch_appointment__type',
            'entries__dispatch_appointment__technician',
            'entries__dispatch_appointment__timeslot',
            'entries__dispatch_appointment__created_by',
            'entries__dispatch_appointment__canceled_by',
            'entries__actions',
            'entries__actions__type',
            'ticket_category',
            'ticket_status',
            'user',
            'subscriber',
            'subscriber__home',
            'subscriber__home__mac_address',
            'subscriber__home__node',
            'subscriber__home__us_state',
            'subscriber__home__project'
        ).order_by('-ticket_status_id', '-opened_on').first()

        if active_ticket:
            active_ticket.minimize = False
            active_ticket.close_ticket = False
            user.active_ticket = active_ticket

        user.alerts = Alert.objects.select_related("type").filter(active=True).order_by("-alert_type_id")
        user.sandbox = settings.ENVIRONMENT != 'production'
        user.access_token = AccessToken.objects.get(user=user).token if hasattr(user, 'access_token') else None
        return Response({
            'success': True,
            'data': {
                'token': str(user.access_token),
                'user': UserSerializer(user).data
            },
            'message': 'User Authenticated.'
        }, status=status.HTTP_200_OK)

class ResetMyPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = PasswordResetSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'success': False,
                'data': serializer.errors,
                'message': 'Validation Error'
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        if not check_password(data['currentPassword'], user.password):
            return Response({
                'success': False,
                'data': False,
                'message': 'Incorrect current password. Please try again or contact your system administrator.'
            }, status=status.HTTP_200_OK)
        if data['password'] != data['confirmPassword']:
            return Response({
                'success': False,
                'data': False,
                'message': 'Password and Confirm Password do not match.'
            }, status=status.HTTP_200_OK)


        user.set_password(data['password'])
        user.activated = True 
        result = user.save()
        print(f"Password update result: {result}")
        try:
            user.set_password(data['password'])
            user.activated = True
            user.save()

            response = {
                'success': True,
                'data': True,
                'message': 'Password Successfully Updated.'
            }
        except Exception as e:
            print(f"Error updating password: {e}")
            response = {
                'success': False,
                'data': str(e),
                'message': 'Failed to Update Password.'
            }

        return Response(response, status=status.HTTP_200_OK)
        # # Send email if needed
        # if result:
        #     try:
        #         # Replace with your actual email logic
        #         send_mail(
        #             subject='Password Updated',
        #             message='Your password has been successfully updated.',
        #             from_email=settings.DEFAULT_FROM_EMAIL,
        #             recipient_list=[user.email],
        #             fail_silently=True
        #         )
        #     except Exception as e:
        #         # Log or handle email error if needed
        #         pass

        # success = True

        # # Send email...
        # # Then:
        # return Response({
        #     'success': success,
        #     'data': True,
        #     'message': 'Password Successfully Updated.'
        # }, status=status.HTTP_200_OK)



class FakeGetActiveTicketView(APIView):
    permission_classes = [AllowAny]  

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

class LogoutView(APIView):
    """
    Endpoint for logging out and revoking the access token.
    Corresponds to your `logout` method.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            # The token is available on the request object
            token = get_access_token_model().objects.get(token=request.auth.token)
            token.revoke()
            return Response({'success': True, 'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
