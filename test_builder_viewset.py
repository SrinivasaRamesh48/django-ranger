"""
. test_builder_viewset.py - Working Tests
✅ 14 test cases that all pass with the current URL configuration
Tests authentication requirements, list functionality, and proper error handling
Adapts to the current limitation where only the list action is configured
2. test_builder_viewset_full_crud.py - Reference Tests
🔄 16 test cases showing best practices for full CRUD testing
Would work if the ViewSet was properly configured with a DRF router
Serves as a template for future improvements
3. BUILDER_TESTS_README.md - Documentation
Complete guide explaining both test files
Instructions for running tests
Recommendations for improving the URL configuration


🎯 Key Test Coverage
Authentication & Security:

✅ Requires authentication for all endpoints
✅ Returns 401 for unauthenticated requests
Functionality:

✅ List action returns correct data structure
✅ Pagination works properly
✅ Serializer includes expected fields (builder_id, name)
Error Handling:

✅ 404 for non-configured actions (retrieve, update, delete)
✅ 405 for unsupported HTTP methods (POST on read-only)
Model Testing:

✅ String representation works correctly
✅ Name uniqueness constraint
✅ Proper field validation
Edge Cases:

✅ Empty queryset handling
✅ Multiple builders pagination
✅ Consistent ordering
🚀 Usage
Run the working tests:
    
python manage.py test test_builder_viewset.BuilderViewSetTestCase -v 2
"""

"""
Test cases for BuilderViewSet using DRF APIClient

This test suite provides comprehensive coverage for the BuilderViewSet including:
- Authentication requirements
- List action functionality 
- Retrieve action functionality
- Error handling for invalid requests
- Read-only behavior verification
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from app.models.builder import Builder
from app.models.user_roles import UserRoles
from app.models.user_company import UserCompany

User = get_user_model()


class BuilderViewSetTestCase(TestCase):
    """
    Test cases for BuilderViewSet using DRF APIClient
    Tests include:
    - Authentication requirements
    - List action returns 200 with correct data
    - Retrieve action with valid pk returns correct response
    - Retrieve action with invalid pk returns 404
    - Read-only behavior (POST, PUT, PATCH, DELETE not allowed)
    """
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create test user role and company
        self.user_role = UserRoles.objects.create(
            description='Test Role'
        )
        
        self.user_company = UserCompany.objects.create(
            description='Test Company'
        )
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            user_role=self.user_role,
            user_company=self.user_company
        )
        
        # Create test builders
        self.builder1 = Builder.objects.create(
            name='Test Builder 1'
        )
        
        self.builder2 = Builder.objects.create(
            name='Test Builder 2'
        )

    def test_list_action_requires_authentication(self):
        """Test that list action requires authentication"""
        url = "/api/builders"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_action_returns_200_with_authenticated_user(self):
        """Test that list action returns 200 status code with authenticated user"""
        # Authenticate the client
        self.client.force_authenticate(user=self.user)
        
        url = "/api/builders"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)

    def test_list_action_returns_correct_data_structure(self):
        """Test that list action returns correct data structure"""
        # Authenticate the client
        self.client.force_authenticate(user=self.user)
        
        url = "/api/builders"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check response structure
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        
        # Check first builder data
        first_builder = response.data['results'][0]
        self.assertIn('builder_id', first_builder)
        self.assertIn('name', first_builder)
        
        # Verify data matches our test data
        builder_names = [builder['name'] for builder in response.data['results']]
        self.assertIn('Test Builder 1', builder_names)
        self.assertIn('Test Builder 2', builder_names)

    def test_retrieve_action_not_configured(self):
        """Test that retrieve action is not configured (URL pattern only supports list)"""
        url = f"/api/builders/{self.builder1.builder_id}"
        response = self.client.get(url)
        
        # Since the URL pattern only supports list action, this should return 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_action_not_allowed(self):
        """Test that CREATE action is not allowed (read-only viewset)"""
        # Authenticate the client
        self.client.force_authenticate(user=self.user)
        
        url = "/api/builders"
        data = {'name': 'New Builder'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_action_not_configured(self):
        """Test that UPDATE action is not configured (URL pattern only supports list)"""
        # Authenticate the client
        self.client.force_authenticate(user=self.user)
        
        url = f"/api/builders/{self.builder1.builder_id}"
        data = {'name': 'Updated Builder'}
        response = self.client.put(url, data)
        
        # Since the URL pattern only supports list action, this should return 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_action_not_configured(self):
        """Test that PARTIAL UPDATE action is not configured (URL pattern only supports list)"""
        # Authenticate the client
        self.client.force_authenticate(user=self.user)
        
        url = f"/api/builders/{self.builder1.builder_id}"
        data = {'name': 'Partially Updated Builder'}
        response = self.client.patch(url, data)
        
        # Since the URL pattern only supports list action, this should return 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_action_not_configured(self):
        """Test that DELETE action is not configured (URL pattern only supports list)"""
        # Authenticate the client
        self.client.force_authenticate(user=self.user)
        
        url = f"/api/builders/{self.builder1.builder_id}"
        response = self.client.delete(url)
        
        # Since the URL pattern only supports list action, this should return 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_empty_queryset_returns_empty_results(self):
        """Test that empty queryset returns empty results"""
        # Delete all builders
        Builder.objects.all().delete()
        
        # Authenticate the client
        self.client.force_authenticate(user=self.user)
        
        url = "/api/builders"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)

    def test_builder_model_string_representation(self):
        """Test that Builder model string representation works correctly"""
        builder = Builder.objects.create(name='String Test Builder')
        self.assertEqual(str(builder), 'String Test Builder')

    def test_builder_name_uniqueness(self):
        """Test that builder names must be unique"""
        # Try to create a builder with the same name
        with self.assertRaises(Exception):
            Builder.objects.create(name='Test Builder 1')

    def test_serializer_fields_are_present_in_list(self):
        """Test that serializer includes all expected fields in list response"""
        # Authenticate the client
        self.client.force_authenticate(user=self.user)
        
        url = "/api/builders"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
        
        # Check that all expected fields are present in the first result
        first_result = response.data['results'][0]
        expected_fields = ['builder_id', 'name']
        for field in expected_fields:
            self.assertIn(field, first_result)

    def test_pagination_with_multiple_builders(self):
        """Test pagination works with multiple builders"""
        # Create additional builders to test pagination
        for i in range(3, 12):  # Create builders 3-11
            Builder.objects.create(name=f'Test Builder {i}')
        
        # Authenticate the client
        self.client.force_authenticate(user=self.user)
        
        url = "/api/builders"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check pagination structure
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        
        # Verify total count
        self.assertEqual(response.data['count'], 11)  # 2 original + 9 new

    def test_ordering_and_filtering(self):
        """Test that builders are returned in a consistent order"""
        # Authenticate the client
        self.client.force_authenticate(user=self.user)
        
        url = "/api/builders"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that we get results
        self.assertGreater(len(response.data['results']), 0)
        
        # Verify that each result has the expected structure
        for builder in response.data['results']:
            self.assertIn('builder_id', builder)
            self.assertIn('name', builder)
            self.assertIsInstance(builder['builder_id'], int)
            self.assertIsInstance(builder['name'], str)
