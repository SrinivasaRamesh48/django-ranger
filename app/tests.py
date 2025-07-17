from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from oauth2_provider.models import Application, AccessToken
from app.models import User, UserRoles, UserCompany, UserPermissionType, UserPermissions, UserPermissionCategory, UserPermissionSubcategory
from django.utils import timezone
from datetime import timedelta


class LoginViewTest(APITestCase):
    def setUp(self):
        # Basic setup for user
        user_role = UserRoles.objects.create(description="Test Role")
        user_company = UserCompany.objects.create(description="Test Company")
        self.user = User.objects.create_user(username='testuser@example.com', password='password', user_role=user_role, user_company=user_company, email='testuser@example.com')
        
        # OAuth2 application
        self.application = Application.objects.create(
            name='Frontend App',
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            user=self.user
        )
        
        self.login_url = reverse('login')

    def test_login_success(self):
        """
        Ensure a user can log in with correct credentials.
        """
        data = {'email': 'testuser@example.com', 'password': 'password'}
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('token', response.data['data'])
        self.assertIn('refresh_token', response.data['data'])
        self.assertEqual(response.data['data']['user']['email'], 'testuser@example.com')

    def test_login_invalid_password(self):
        """
        Ensure login fails with an incorrect password.
        """
        data = {'email': 'testuser@example.com', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['message'], 'Invalid credentials')

    def test_login_nonexistent_user(self):
        """
        Ensure login fails for a user that does not exist.
        """
        data = {'email': 'nouser@example.com', 'password': 'password'}
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['message'], 'Invalid credentials')

    def test_login_inactive_user(self):
        """
        Ensure an inactive user cannot log in.
        """
        self.user.is_active = False
        self.user.save()
        
        data = {'email': 'testuser@example.com', 'password': 'password'}
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['message'], 'Invalid credentials')

    def test_login_missing_credentials(self):
        """
        Ensure login fails if email or password is not provided.
        """
        # Missing password
        data = {'email': 'testuser@example.com'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Missing email
        data = {'password': 'password'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthenticateViewTest(APITestCase):
    def setUp(self):
        self.user_role = UserRoles.objects.create(description="Test Role")
        self.user_company = UserCompany.objects.create(description="Test Company")
        self.user = User.objects.create_user(
            username='testauth@example.com',
            password='password',
            user_role=self.user_role,
            user_company=self.user_company,
            email='testauth@example.com'
        )
        self.application = Application.objects.create(
            name='Test App for Auth',
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            user=self.user
        )
        self.token = AccessToken.objects.create(
            user=self.user,
            application=self.application,
            token='a-test-token-for-auth-view',
            expires=timezone.now() + timedelta(days=1),
            scope='read write'
        )
        self.authenticate_url = reverse('authenticate')

    def test_authenticate_success(self):
        """
        Ensure an authenticated user can get their details.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.token}')
        response = self.client.get(self.authenticate_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['user']['email'], self.user.email)
        self.assertIn('token', response.data['data'])

    def test_authenticate_inactive_user(self):
        """
        Ensure an inactive user cannot authenticate.
        """
        self.user.is_active = False
        self.user.save()
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.token}')
        response = self.client.get(self.authenticate_url)
        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertFalse(response.data['success'])

    def test_authenticate_unauthenticated(self):
        """
        Ensure an unauthenticated request is rejected.
        """
        response = self.client.get(self.authenticate_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TechnicianViewSetTest(APITestCase):
    def setUp(self):
        self.user_role = UserRoles.objects.create(description="Admin Role")
        self.user_company = UserCompany.objects.create(description="Main Company")
        
        # Admin user to perform actions
        self.admin_user = User.objects.create_user(
            username='admin@example.com', password='password', user_role=self.user_role, 
            user_company=self.user_company, email='admin@example.com', is_staff=True
        )
        
        # Technician user to be managed
        self.technician_role = UserRoles.objects.create(description="Technician Role")
        self.technician = User.objects.create_user(
            username='tech@example.com', password='password', user_role=self.technician_role,
            user_company=self.user_company, email='tech@example.com', name='Tech One'
        )

        self.application = Application.objects.create(
            name='Test App for Technicians',
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            user=self.admin_user
        )
        self.token = AccessToken.objects.create(
            user=self.admin_user,
            application=self.application,
            token='a-test-token-for-technician-view',
            expires=timezone.now() + timedelta(days=1),
            scope='read write'
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.token}')

    def test_list_technicians(self):
        url = reverse('technician-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_retrieve_technician(self):
        url = reverse('technician-detail', kwargs={'pk': self.technician.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.technician.email)

    def test_update_technician(self):
        url = reverse('technician-detail', kwargs={'pk': self.technician.pk})
        data = {'name': 'Tech One Updated'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.technician.refresh_from_db()
        self.assertEqual(self.technician.name, 'Tech One Updated')

    def test_reset_password(self):
        url = reverse('technician-reset-password', kwargs={'pk': self.technician.pk})
        old_password = self.technician.password
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.technician.refresh_from_db()
        self.assertNotEqual(old_password, self.technician.password)
        self.assertFalse(self.technician.activated)

    def test_update_permissions(self):
        category = UserPermissionCategory.objects.create(description='Test Category')
        permission = UserPermissionType.objects.create(
            identifier='test_permission', 
            description='Test Permission',
            user_permission_category=category
        )
        url = reverse('technician-update-permissions', kwargs={'pk': self.technician.pk})
        data = {'permission_identifiers': [permission.identifier]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        has_permission = UserPermissions.objects.filter(user=self.technician, user_permission_type=permission).exists()
        self.assertTrue(has_permission)

    def test_unauthenticated_access(self):
        self.client.credentials()  # Clear credentials
        url = reverse('technician-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PermissionTypesViewTest(APITestCase):
    def setUp(self):
        self.user_role = UserRoles.objects.create(description="Test Role for Permissions")
        self.user_company = UserCompany.objects.create(description="Test Company for Permissions")
        self.user = User.objects.create_user(
            username='perm_test@example.com', password='password',
            user_role=self.user_role, user_company=self.user_company
        )
        self.application = Application.objects.create(
            name='Test App for Permissions',
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            user=self.user
        )
        self.token = AccessToken.objects.create(
            user=self.user,
            application=self.application,
            token='a-test-token-for-permission-types-view',
            expires=timezone.now() + timedelta(days=1),
            scope='read write'
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.token}')
        self.url = reverse('permission-types')

    def test_get_permission_types_success(self):
        """
        Ensure we can retrieve a list of permission types.
        """
        category = UserPermissionCategory.objects.create(description='General')
        subcategory = UserPermissionSubcategory.objects.create(description='Sub General', user_permission_category=category)
        UserPermissionType.objects.create(
            identifier='view_dashboard', description='View Dashboard',
            user_permission_category=category, user_permission_subcategory=subcategory
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['identifier'], 'view_dashboard')

    def test_get_permission_types_empty(self):
        """
        Ensure the endpoint handles having no permission types.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['success'])
        self.assertEqual(len(response.data['data']), 0)

    def test_get_permission_types_unauthenticated(self):
        """
        Ensure unauthenticated users cannot access the endpoint.
        """
        self.client.credentials()  # Clear authentication
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
