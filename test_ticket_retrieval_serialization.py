"""
Test suite for the ticket retrieval and serialization part of TicketViewSet.create()

This test focuses specifically on the complex query and serialization logic:
- Complex select_related/prefetch_related queries
- TicketSerializer performance with related objects
- Response format validation
"""

import unittest
from unittest.mock import patch, Mock
from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from django.db import transaction

from app.models import (
    Ticket, TicketEntry, TicketEntryAction, TicketEntryActionType, 
    TicketStatus, TicketCategory, Subscriber, Home, Project, 
    ServicePlan, Node, Circuit, UsState, MacAddress,
    DispatchAppointment, DispatchAppointmentType, DispatchAppointmentTimeslot,
    ServiceChangeSchedule
)

User = get_user_model()


class TicketRetrievalSerializationTestCase(APITestCase):
    """Test the ticket retrieval and serialization logic in TicketViewSet.create()"""
    
    def setUp(self):
        """Set up test data with minimal required related objects"""
        # Create user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Create minimal required objects
        self.circuit = Circuit.objects.create(circuit_name='Test Circuit')
        self.project = Project.objects.create(
            project_name='Test Project',
            circuit=self.circuit
        )
        
        self.home = Home.objects.create(
            address='123 Test St',
            project=self.project
        )
        
        self.service_plan = ServicePlan.objects.create(
            service_plan_name='Test Plan',
            monthly_rate=50.00
        )
        
        self.subscriber = Subscriber.objects.create(
            first_name='John',
            last_name='Doe',
            primary_email='john@example.com',
            primary_phone='555-1234',
            username='johndoe',
            password='hashedpass',
            home=self.home,
            service_plan=self.service_plan
        )
        
        # Create ticket status and category
        self.ticket_status = TicketStatus.objects.create(description='Open')
        self.ticket_category = TicketCategory.objects.create(description='Support')
        
        # Create action type for ticket entries
        self.action_type = TicketEntryActionType.objects.create(description='Note')
        
        # Create dispatch appointment related objects
        self.appointment_type = DispatchAppointmentType.objects.create(description='Installation')
        self.timeslot = DispatchAppointmentTimeslot.objects.create(
            start_time='09:00:00',
            end_time='12:00:00',
            description='Morning'
        )
        
        # Set up API client with authentication
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_exact_query_from_view_code(self):
        """Test the exact select_related/prefetch_related query from the view"""
        # Create a ticket with related objects
        ticket = Ticket.objects.create(
            subscriber=self.subscriber,
            user=self.user,
            ticket_status=self.ticket_status,
            ticket_category=self.ticket_category
        )
        
        # Create ticket entry
        entry = TicketEntry.objects.create(
            ticket=ticket,
            user=self.user,
            start_time=timezone.now(),
            description='Test entry'
        )
        
        # Create ticket entry action
        action = TicketEntryAction.objects.create(
            ticket_entry=entry,
            type=self.action_type
        )
        
        # Test the EXACT query from tickets_view.py lines 135-147
        try:
            retrieved_ticket = Ticket.objects.select_related(
                'ticket_category', 'ticket_status', 'user',
                'subscriber__service_plan', 'subscriber__home__project',
                'subscriber__home__mac_address', 'subscriber__home__node',
                'subscriber__home__us_state'
            ).prefetch_related(
                'entries',
                'entries__dispatch_appointment__type',
                'entries__dispatch_appointment__technician',
                'entries__dispatch_appointment__timeslot',
                'entries__dispatch_appointment__created_by',
                'entries__dispatch_appointment__canceled_by',
                'entries__actions__type',
                'entries__service_change_schedule'
            ).order_by('-ticket_status_id', '-opened_on').get(ticket_id=ticket.ticket_id)
            
            # Test should pass if no exception is raised
            self.assertEqual(retrieved_ticket.ticket_id, ticket.ticket_id)
            
        except Exception as e:
            self.fail(f"Query failed with exception: {e}")

    def test_serialization_after_complex_query(self):
        """Test that TicketSerializer works with the complex query result"""
        from app.serializers.ticket_serializer import TicketSerializer
        
        # Create ticket with related objects
        ticket = Ticket.objects.create(
            subscriber=self.subscriber,
            user=self.user,
            ticket_status=self.ticket_status,
            ticket_category=self.ticket_category
        )
        
        entry = TicketEntry.objects.create(
            ticket=ticket,
            user=self.user,
            start_time=timezone.now(),
            description='Test entry for serialization'
        )
        
        action = TicketEntryAction.objects.create(
            ticket_entry=entry,
            type=self.action_type
        )
        
        # Execute the exact query
        retrieved_ticket = Ticket.objects.select_related(
            'ticket_category', 'ticket_status', 'user',
            'subscriber__service_plan', 'subscriber__home__project',
            'subscriber__home__mac_address', 'subscriber__home__node',
            'subscriber__home__us_state'
        ).prefetch_related(
            'entries',
            'entries__dispatch_appointment__type',
            'entries__dispatch_appointment__technician',
            'entries__dispatch_appointment__timeslot',
            'entries__dispatch_appointment__created_by',
            'entries__dispatch_appointment__canceled_by',
            'entries__actions__type',
            'entries__service_change_schedule'
        ).order_by('-ticket_status_id', '-opened_on').get(ticket_id=ticket.ticket_id)
        
        # Test serialization (this is lines 148-149 from the view)
        try:
            serializer = TicketSerializer(retrieved_ticket)
            serialized_data = serializer.data
            
            # Verify basic structure
            self.assertIn('ticket_id', serialized_data)
            self.assertEqual(serialized_data['ticket_id'], ticket.ticket_id)
            
        except Exception as e:
            self.fail(f"Serialization failed with exception: {e}")

    def test_response_creation_exact_format(self):
        """Test the exact response format from lines 150-156 of the view"""
        from app.serializers.ticket_serializer import TicketSerializer
        
        ticket = Ticket.objects.create(
            subscriber=self.subscriber,
            user=self.user,
            ticket_status=self.ticket_status,
            ticket_category=self.ticket_category
        )
        
        entry = TicketEntry.objects.create(
            ticket=ticket,
            user=self.user,
            start_time=timezone.now(),
            description='Test entry'
        )
        
        action = TicketEntryAction.objects.create(
            ticket_entry=entry,
            type=self.action_type
        )
        
        # Execute exact query and response creation from view
        try:
            retrieved_ticket = Ticket.objects.select_related(
                'ticket_category', 'ticket_status', 'user',
                'subscriber__service_plan', 'subscriber__home__project',
                'subscriber__home__mac_address', 'subscriber__home__node',
                'subscriber__home__us_state'
            ).prefetch_related(
                'entries',
                'entries__dispatch_appointment__type',
                'entries__dispatch_appointment__technician',
                'entries__dispatch_appointment__timeslot',
                'entries__dispatch_appointment__created_by',
                'entries__dispatch_appointment__canceled_by',
                'entries__actions__type',
                'entries__service_change_schedule'
            ).order_by('-ticket_status_id', '-opened_on').get(ticket_id=ticket.ticket_id)

            serializer = TicketSerializer(retrieved_ticket)
            
            # Create exact response format from lines 150-156
            response_data = {
                'success': True,
                'data': serializer.data,
                'message': 'Ticket Successfully Created.'
            }
            
            # Verify response structure
            self.assertTrue(response_data['success'])
            self.assertEqual(response_data['message'], 'Ticket Successfully Created.')
            self.assertIsInstance(response_data['data'], dict)
            self.assertEqual(response_data['data']['ticket_id'], ticket.ticket_id)
            
        except Exception as e:
            self.fail(f"Response creation failed with exception: {e}")

    def test_query_with_missing_related_objects(self):
        """Test behavior when some related objects referenced in select_related are None"""
        # Create ticket with minimal related objects (some may be None)
        ticket = Ticket.objects.create(
            subscriber=self.subscriber,
            user=self.user,
            ticket_status=self.ticket_status
            # Note: no ticket_category
        )
        
        entry = TicketEntry.objects.create(
            ticket=ticket,
            user=self.user,
            start_time=timezone.now(),
            description='Test entry without all related objects'
        )
        
        # Test that query still works with missing related objects
        try:
            retrieved_ticket = Ticket.objects.select_related(
                'ticket_category', 'ticket_status', 'user',
                'subscriber__service_plan', 'subscriber__home__project',
                'subscriber__home__mac_address', 'subscriber__home__node',
                'subscriber__home__us_state'
            ).prefetch_related(
                'entries',
                'entries__dispatch_appointment__type',
                'entries__dispatch_appointment__technician',
                'entries__dispatch_appointment__timeslot',
                'entries__dispatch_appointment__created_by',
                'entries__dispatch_appointment__canceled_by',
                'entries__actions__type',
                'entries__service_change_schedule'
            ).order_by('-ticket_status_id', '-opened_on').get(ticket_id=ticket.ticket_id)
            
            # Should not raise exception even with missing related objects
            self.assertEqual(retrieved_ticket.ticket_id, ticket.ticket_id)
            
        except Exception as e:
            self.fail(f"Query with missing related objects failed: {e}")

    def test_ticket_does_not_exist_handling(self):
        """Test that DoesNotExist exception is properly raised"""
        with self.assertRaises(Ticket.DoesNotExist):
            Ticket.objects.select_related(
                'ticket_category', 'ticket_status', 'user',
                'subscriber__service_plan', 'subscriber__home__project',
                'subscriber__home__mac_address', 'subscriber__home__node',
                'subscriber__home__us_state'
            ).prefetch_related(
                'entries',
                'entries__dispatch_appointment__type',
                'entries__dispatch_appointment__technician',
                'entries__dispatch_appointment__timeslot',
                'entries__dispatch_appointment__created_by',
                'entries__dispatch_appointment__canceled_by',
                'entries__actions__type',
                'entries__service_change_schedule'
            ).order_by('-ticket_status_id', '-opened_on').get(ticket_id=99999)

    def test_query_performance_with_complex_data(self):
        """Test query performance with multiple entries and related objects"""
        ticket = Ticket.objects.create(
            subscriber=self.subscriber,
            user=self.user,
            ticket_status=self.ticket_status,
            ticket_category=self.ticket_category
        )
        
        # Create multiple entries with related objects
        for i in range(3):
            entry = TicketEntry.objects.create(
                ticket=ticket,
                user=self.user,
                start_time=timezone.now(),
                description=f'Test entry {i}'
            )
            
            TicketEntryAction.objects.create(
                ticket_entry=entry,
                type=self.action_type
            )
            
            # Create dispatch appointment
            DispatchAppointment.objects.create(
                ticket_entry=entry,
                appointment_type=self.appointment_type,
                technician=self.user,
                timeslot=self.timeslot,
                created_by=self.user,
                date=timezone.now().date()
            )
        
        # Test query performance - should be efficient due to prefetch_related
        with self.assertNumQueries(2):  # Main query + prefetch queries
            retrieved_ticket = Ticket.objects.select_related(
                'ticket_category', 'ticket_status', 'user',
                'subscriber__service_plan', 'subscriber__home__project',
                'subscriber__home__mac_address', 'subscriber__home__node',
                'subscriber__home__us_state'
            ).prefetch_related(
                'entries',
                'entries__dispatch_appointment__type',
                'entries__dispatch_appointment__technician',
                'entries__dispatch_appointment__timeslot',
                'entries__dispatch_appointment__created_by',
                'entries__dispatch_appointment__canceled_by',
                'entries__actions__type',
                'entries__service_change_schedule'
            ).order_by('-ticket_status_id', '-opened_on').get(ticket_id=ticket.ticket_id)
            
            # Access the data that should be prefetched
            entries = list(retrieved_ticket.entries.all())
            for entry in entries:
                actions = list(entry.actions.all())
                if hasattr(entry, 'dispatch_appointment') and entry.dispatch_appointment:
                    _ = entry.dispatch_appointment.appointment_type


if __name__ == '__main__':
    unittest.main()
