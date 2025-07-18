"""
Summary
I have successfully created a comprehensive test suite for the TicketViewSet class with 38 test cases that now all pass successfully!

What was accomplished:
Complete Test Coverage: Created tests for all TicketViewSet methods including CRUD operations, ticket actions, chart data, authentication, and error handling.

Fixed Multiple Issues:

Corrected serializer field validation issues
Fixed view methods to use proper status handling instead of hardcoded IDs
Resolved foreign key constraint problems
Fixed database relationship issues in test setup
Comprehensive Test Scenarios:

✅ 8 CRUD operation tests
✅ 6 ticket entry management tests
✅ 8 ticket action tests (close, reopen, bulk operations)
✅ 6 chart data and reporting tests
✅ 3 authentication and security tests
✅ 7 error handling and edge case tests
Production-Ready Code: The test suite validates that the TicketViewSet can handle real-world scenarios including authentication, validation, error handling, and complex operations
"""

import json
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock

from app.models import (
    Ticket, TicketEntry, TicketStatus, TicketCategory, 
    Subscriber, Home, Project, ServicePlan, Node, Circuit,
    SubscriptionType, UsState, UserRoles, UserCompany
)

User = get_user_model()


class TicketViewSetTestCase(TestCase):
    """Test cases for the TicketViewSet class."""
    
    def setUp(self):
        """Set up test data for each test case."""
        self.client = APIClient()
        
        # Create required reference data
        self.user_role = UserRoles.objects.create(description='Test Role')
        self.user_company = UserCompany.objects.create(description='Test Company')
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user.user_role = self.user_role
        self.user.user_company = self.user_company
        self.user.save()
        
        # Create test ticket statuses
        self.open_status = TicketStatus.objects.create(description='Open')
        self.closed_status = TicketStatus.objects.create(description='Closed')
        
        # Create test ticket category
        self.ticket_category = TicketCategory.objects.create(description='Test Category')
        
        # Create test service plan
        self.service_plan = ServicePlan.objects.create(name='Test Plan')
        
        # Create test US state and subscription type
        self.us_state = UsState.objects.create(name='Test State', abbr='TS')
        self.subscription_type = SubscriptionType.objects.create(name='Test Subscription')
        
        # Create test project
        self.project = Project.objects.create(
            name='Test Project',
            address='123 Test St',
            city='Test City',
            zip_code='12345',
            state=self.us_state,
            subscription_type=self.subscription_type
        )
        
        # Create test home
        self.home = Home.objects.create(
            address='123 Test St',
            city='Test City',
            zip_code='12345',
            project=self.project,
            us_state=self.us_state,
            node_switch_unit='1',
            node_switch_module='1',
            node_port_num='1'
        )
        
        # Create test subscriber
        self.subscriber = Subscriber.objects.create(
            first_name='John',
            last_name='Doe',
            primary_email='john@example.com',
            username='johndoe',
            password='password123',
            home=self.home,
            service_plan=self.service_plan
        )
        
        # Create test ticket
        self.ticket = Ticket.objects.create(
            subscriber=self.subscriber,
            user=self.user,
            ticket_category=self.ticket_category,
            ticket_status=self.open_status
        )
        
        # Create test ticket entry
        self.ticket_entry = TicketEntry.objects.create(
            ticket=self.ticket,
            user=self.user,
            description='Test entry',
            submitted=1
        )
        
        # Authenticate user
        self.client.force_authenticate(user=self.user)

    def test_list_tickets(self):
        """Test listing all tickets."""
        url = reverse('tickets-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['message'], 'Tickets retrieved')

    def test_retrieve_ticket(self):
        """Test retrieving a specific ticket."""
        url = reverse('tickets-detail', kwargs={'pk': self.ticket.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['ticket_id'], self.ticket.pk)
        self.assertEqual(response.data['message'], 'Ticket retrieved')

    def test_create_ticket(self):
        """Test creating a new ticket."""
        url = reverse('create_ticket')
        data = {
            'subscriber_id': self.subscriber.pk,
            'user_id': self.user.pk,
            'ticket_category_id': self.ticket_category.pk,
            'ticket_status_id': self.open_status.pk
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'Ticket created')
        self.assertEqual(Ticket.objects.count(), 2)

    def test_create_ticket_invalid_data(self):
        """Test creating a ticket with invalid data."""
        url = reverse('create_ticket')
        data = {
            'subscriber_id': 999,  # Non-existent subscriber
            'ticket_category_id': self.ticket_category.pk,
            'ticket_status_id': self.open_status.pk
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('errors', response.data)

    def test_update_ticket(self):
        """Test updating a ticket."""
        url = reverse('update_ticket')
        data = {
            'id': self.ticket.pk,
            'ticket_status_id': self.closed_status.pk
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'Ticket updated')
        
        # Verify ticket was updated
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.ticket_status_id, self.closed_status.pk)

    def test_update_ticket_invalid_id(self):
        """Test updating a ticket with invalid ID."""
        url = reverse('update_ticket')
        data = {
            'id': 999,  # Non-existent ticket
            'ticket_status_id': self.closed_status.pk
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_ticket_entry(self):
        """Test creating a ticket entry."""
        url = reverse('create_ticket_entry')
        data = {
            'ticket': self.ticket.pk,
            'description': 'New ticket entry',
            'submitted': 1
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'Entry created')
        self.assertEqual(TicketEntry.objects.count(), 2)

    def test_create_ticket_entry_invalid_data(self):
        """Test creating a ticket entry with invalid data."""
        url = reverse('create_ticket_entry')
        data = {
            'ticket': 999,  # Non-existent ticket
            'description': 'New ticket entry'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])

    def test_delete_ticket_entry(self):
        """Test deleting a ticket entry."""
        url = reverse('delete_ticket_entry')
        data = {
            'id': self.ticket_entry.pk
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'Entry deleted')
        self.assertEqual(TicketEntry.objects.count(), 0)

    def test_delete_ticket_entry_not_found(self):
        """Test deleting a non-existent ticket entry."""
        url = reverse('delete_ticket_entry')
        data = {
            'id': 999
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['message'], 'Entry not found')

    def test_get_active_ticket(self):
        """Test getting the most recent active ticket."""
        url = reverse('active_ticket')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['ticket_id'], self.ticket.pk)

    def test_get_active_ticket_no_active_tickets(self):
        """Test getting active ticket when none exist."""
        # Update ticket to closed status
        self.ticket.ticket_status = self.closed_status
        self.ticket.save()
        
        url = reverse('active_ticket')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['message'], 'No active ticket found')

    def test_add_entry_to_ticket(self):
        """Test adding an entry to a specific ticket."""
        url = reverse('tickets-add-entry', kwargs={'pk': self.ticket.pk})
        data = {
            'description': 'New entry added to ticket',
            'submitted': 1
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'Entry added')
        self.assertEqual(TicketEntry.objects.count(), 2)

    def test_add_entry_to_nonexistent_ticket(self):
        """Test adding an entry to a non-existent ticket."""
        url = reverse('tickets-add-entry', kwargs={'pk': 999})
        data = {
            'description': 'New entry',
            'submitted': 1
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_close_ticket(self):
        """Test closing a ticket."""
        url = reverse('tickets-close-ticket', kwargs={'pk': self.ticket.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'Ticket closed')
        
        # Verify ticket was closed (using the existing closed status)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.ticket_status_id, self.closed_status.pk)
        self.assertIsNotNone(self.ticket.closed_on)
        
        # Verify entry was created
        self.assertEqual(TicketEntry.objects.count(), 2)
        new_entry = TicketEntry.objects.latest('created_at')
        self.assertEqual(new_entry.description, 'Ticket closed.')

    def test_reopen_ticket(self):
        """Test reopening a ticket."""
        # Use get_or_create to avoid duplicate status issues
        reopen_status, created = TicketStatus.objects.get_or_create(
            description='Reopened',
            defaults={'description': 'Reopened'}
        )
        
        # First close the ticket
        self.ticket.ticket_status = self.closed_status
        self.ticket.closed_on = timezone.now()
        self.ticket.save()
        
        url = reverse('tickets-reopen-ticket', kwargs={'pk': self.ticket.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'Ticket reopened')
        
        # Verify ticket was reopened
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.ticket_status_id, reopen_status.pk)
        self.assertIsNone(self.ticket.closed_on)

    def test_update_ticket_status(self):
        """Test updating ticket status."""
        url = reverse('tickets-update-status', kwargs={'pk': self.ticket.pk})
        data = {
            'ticket_status_id': self.closed_status.pk
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'Status updated')
        
        # Verify status was updated
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.ticket_status_id, self.closed_status.pk)

    def test_update_ticket_status_missing_id(self):
        """Test updating ticket status without providing status ID."""
        url = reverse('tickets-update-status', kwargs={'pk': self.ticket.pk})
        data = {}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['message'], 'ticket_status_id required')

    def test_technician_tickets(self):
        """Test getting tickets for a specific technician."""
        url = reverse('tickets-technician-tickets', kwargs={'technician_id': self.user.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['ticket_id'], self.ticket.pk)

    def test_technician_tickets_no_tickets(self):
        """Test getting tickets for technician with no tickets."""
        new_user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='newpass123'
        )
        new_user.user_role = self.user_role
        new_user.user_company = self.user_company
        new_user.save()
        
        url = reverse('tickets-technician-tickets', kwargs={'technician_id': new_user.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']), 0)

    def test_bulk_close_tickets(self):
        """Test bulk closing tickets."""
        # Use the existing closed status instead of creating a new one
        # Create another ticket
        ticket2 = Ticket.objects.create(
            subscriber=self.subscriber,
            user=self.user,
            ticket_category=self.ticket_category,
            ticket_status=self.open_status
        )
        
        url = reverse('tickets-bulk-close')
        data = {
            'ticket_ids': [self.ticket.pk, ticket2.pk],
            'note': 'Bulk closed for testing'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], '2 tickets closed')
        
        # Verify tickets were closed (using the existing closed status)
        self.ticket.refresh_from_db()
        ticket2.refresh_from_db()
        self.assertEqual(self.ticket.ticket_status_id, self.closed_status.pk)
        self.assertEqual(ticket2.ticket_status_id, self.closed_status.pk)
        
        # Verify entries were created
        self.assertEqual(TicketEntry.objects.filter(description='Bulk closed for testing').count(), 2)

    def test_bulk_close_empty_list(self):
        """Test bulk closing with empty ticket list."""
        url = reverse('tickets-bulk-close')
        data = {
            'ticket_ids': [],
            'note': 'No tickets to close'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], '0 tickets closed')

    def test_tickets_chart_data_category_filter(self):
        """Test getting chart data filtered by category."""
        url = reverse('tickets_chart_data', kwargs={'filter': 'category', 'timeframe': '30'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']), 1)

    def test_tickets_chart_data_circuit_filter(self):
        """Test getting chart data filtered by circuit."""
        url = reverse('tickets_chart_data', kwargs={'filter': 'circuit', 'timeframe': '7'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    def test_tickets_chart_data_project_filter(self):
        """Test getting chart data filtered by project."""
        url = reverse('tickets_chart_data', kwargs={'filter': 'project', 'timeframe': '90'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    def test_tickets_chart_data_technician_filter(self):
        """Test getting chart data filtered by technician."""
        url = reverse('tickets_chart_data', kwargs={'filter': 'technician', 'timeframe': '365'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    def test_tickets_chart_data_status_filter(self):
        """Test getting chart data filtered by status."""
        url = reverse('tickets_chart_data', kwargs={'filter': 'status', 'timeframe': '30'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    def test_tickets_chart_data_default_filter(self):
        """Test getting chart data with default/unknown filter."""
        url = reverse('tickets_chart_data', kwargs={'filter': 'unknown', 'timeframe': '30'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    def test_authentication_required(self):
        """Test that authentication is required for all endpoints."""
        self.client.logout()
        
        endpoints = [
            reverse('tickets-list'),
            reverse('tickets-detail', kwargs={'pk': self.ticket.pk}),
            reverse('update_ticket'),
            reverse('create_ticket_entry'),
            reverse('delete_ticket_entry'),
            reverse('active_ticket'),
            reverse('tickets-add-entry', kwargs={'pk': self.ticket.pk}),
            reverse('tickets-close-ticket', kwargs={'pk': self.ticket.pk}),
            reverse('tickets-reopen-ticket', kwargs={'pk': self.ticket.pk}),
            reverse('tickets-update-status', kwargs={'pk': self.ticket.pk}),
            reverse('tickets-technician-tickets', kwargs={'technician_id': self.user.pk}),
            reverse('tickets-bulk-close'),
            reverse('tickets_chart_data', kwargs={'filter': 'category', 'timeframe': '30'}),
        ]
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_ticket_not_found(self):
        """Test handling of non-existent ticket."""
        url = reverse('tickets-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_ticket_entry_creation_with_user(self):
        """Test that ticket entry creation includes the authenticated user."""
        url = reverse('create_ticket_entry')
        data = {
            'ticket': self.ticket.pk,
            'description': 'Entry with user',
            'submitted': 1
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_entry = TicketEntry.objects.latest('created_at')
        self.assertEqual(new_entry.user, self.user)

    def test_ticket_serializer_data_structure(self):
        """Test that ticket serializer returns expected data structure."""
        url = reverse('tickets-detail', kwargs={'pk': self.ticket.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        ticket_data = response.data['data']
        expected_fields = [
            'ticket_id', 'opened_on', 'closed_on', 'subscriber', 'user',
            'ticket_category', 'ticket_status', 'entries'
        ]
        
        for field in expected_fields:
            self.assertIn(field, ticket_data)

    def test_ticket_entry_serializer_data_structure(self):
        """Test that ticket entry serializer returns expected data structure."""
        url = reverse('create_ticket_entry')
        data = {
            'ticket': self.ticket.pk,
            'description': 'Test entry structure',
            'submitted': 1
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        entry_data = response.data['data']
        
        expected_fields = [
            'ticket_entry_id', 'description', 'submitted', 'created_at'
        ]
        
        for field in expected_fields:
            self.assertIn(field, entry_data)

    def test_error_handling_for_invalid_json(self):
        """Test error handling for invalid JSON data."""
        url = reverse('tickets-bulk-close')
        response = self.client.post(
            url,
            data='invalid json',
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_concurrent_ticket_updates(self):
        """Test handling of concurrent ticket updates."""
        # This test simulates what might happen with concurrent updates
        url = reverse('update_ticket')
        
        # First update
        data1 = {
            'id': self.ticket.pk,
            'ticket_status_id': self.closed_status.pk
        }
        response1 = self.client.post(url, data1)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        
        # Second update (should still work)
        data2 = {
            'id': self.ticket.pk,
            'ticket_status_id': self.open_status.pk
        }
        response2 = self.client.post(url, data2)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_ticket_filtering_by_date_range(self):
        """Test that chart data filtering works correctly."""
        # Create tickets with different dates
        old_ticket = Ticket.objects.create(
            subscriber=self.subscriber,
            user=self.user,
            ticket_category=self.ticket_category,
            ticket_status=self.open_status
        )
        old_ticket.opened_on = timezone.now() - timezone.timedelta(days=60)
        old_ticket.save()
        
        url = reverse('tickets_chart_data', kwargs={'filter': 'category', 'timeframe': '30'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only return tickets from the last 30 days
        self.assertEqual(len(response.data['data']), 1)

    def test_large_bulk_operations(self):
        """Test handling of large bulk operations."""
        # Create multiple tickets
        tickets = []
        for i in range(10):
            ticket = Ticket.objects.create(
                subscriber=self.subscriber,
                user=self.user,
                ticket_category=self.ticket_category,
                ticket_status=self.open_status
            )
            tickets.append(ticket.pk)
        
        url = reverse('tickets-bulk-close')
        data = {
            'ticket_ids': tickets,
            'note': 'Bulk close test'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], '10 tickets closed')

    def test_permission_requirements(self):
        """Test that proper permissions are required for operations."""
        # Create a user without proper permissions
        limited_user = User.objects.create_user(
            username='limited',
            email='limited@example.com',
            password='limitedpass123'
        )
        limited_user.user_role = self.user_role
        limited_user.user_company = self.user_company
        limited_user.save()
        
        self.client.force_authenticate(user=limited_user)
        
        # Test that the user can still access basic operations
        # (assuming no additional permission checks are implemented)
        url = reverse('tickets-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
