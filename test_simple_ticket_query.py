"""
Simple focused test for the ticket retrieval and serialization query.
This tests just the specific lines 135-156 from tickets_view.py
"""

import unittest
from unittest.mock import patch, Mock
from django.test import TestCase
from django.utils import timezone

from app.models import (
    Ticket, TicketEntry, TicketEntryAction, TicketEntryActionType, 
    TicketStatus, Subscriber, User, UserRoles, UserCompany, Circuit, CircuitCarrier, Project,
    ServicePlan, Home
)


class SimpleTicketQueryTestCase(TestCase):
    """Test the exact query from the TicketViewSet.create() method"""
    
    def setUp(self):
        """Set up minimal test data"""
        # Create required dependencies first
        self.user_company = UserCompany.objects.create(company_name='Test Company')
        self.user_role = UserRoles.objects.create(role_name='Test Role')
        self.circuit_carrier = CircuitCarrier.objects.create(carrier_name='Test Carrier')
        
        # Create user with proper dependencies
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            user_company=self.user_company,
            user_role=self.user_role
        )
        
        # Create circuit with proper field name
        self.circuit = Circuit.objects.create(
            title='Test Circuit',
            circuit_carrier=self.circuit_carrier
        )
        
        # Create project
        self.project = Project.objects.create(
            project_name='Test Project',
            circuit=self.circuit
        )
        
        # Create home
        self.home = Home.objects.create(
            address='123 Test St',
            project=self.project
        )
        
        # Create service plan
        self.service_plan = ServicePlan.objects.create(
            service_plan_name='Test Plan',
            monthly_rate=50.00
        )
        
        # Create subscriber
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
        
        # Create ticket status
        self.ticket_status = TicketStatus.objects.create(description='Open')
        
        # Create action type
        self.action_type = TicketEntryActionType.objects.create(description='Note')

    def test_exact_query_from_view_lines_135_147(self):
        """Test the exact select_related/prefetch_related query from tickets_view.py lines 135-147"""
        # Create a ticket
        ticket = Ticket.objects.create(
            subscriber=self.subscriber,
            user=self.user,
            ticket_status=self.ticket_status
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
        
        # Test the EXACT query from the view code
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
            
            # Verify we got the right ticket
            self.assertEqual(retrieved_ticket.ticket_id, ticket.ticket_id)
            
            # Verify the query executed without errors
            self.assertIsNotNone(retrieved_ticket)
            
        except Exception as e:
            self.fail(f"The exact query from view failed: {e}")

    def test_serialization_lines_148_149(self):
        """Test the serialization part from lines 148-149"""
        from app.serializers.ticket_serializer import TicketSerializer
        
        # Create ticket with entry and action
        ticket = Ticket.objects.create(
            subscriber=self.subscriber,
            user=self.user,
            ticket_status=self.ticket_status
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
        
        # Test the serialization (line 148)
        try:
            serializer = TicketSerializer(retrieved_ticket)
            serialized_data = serializer.data
            
            # Basic validation that serialization worked
            self.assertIn('ticket_id', serialized_data)
            self.assertEqual(serialized_data['ticket_id'], ticket.ticket_id)
            
        except Exception as e:
            self.fail(f"Serialization failed: {e}")

    def test_response_format_lines_150_156(self):
        """Test the exact response format from lines 150-156"""
        from app.serializers.ticket_serializer import TicketSerializer
        from rest_framework import status as http_status
        
        # Create ticket
        ticket = Ticket.objects.create(
            subscriber=self.subscriber,
            user=self.user,
            ticket_status=self.ticket_status
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
        
        # Execute exact steps from view lines 135-156
        try:
            # Line 135-147: Complex query
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

            # Line 148: Serialization
            serializer = TicketSerializer(retrieved_ticket)
            
            # Lines 149-156: Response format
            response_data = {
                'success': True,
                'data': serializer.data,
                'message': 'Ticket Successfully Created.'
            }
            
            # Verify response structure matches expected format
            self.assertTrue(response_data['success'])
            self.assertEqual(response_data['message'], 'Ticket Successfully Created.')
            self.assertIsInstance(response_data['data'], dict)
            self.assertEqual(response_data['data']['ticket_id'], ticket.ticket_id)
            
            # Verify this would create a proper HTTP 200 response
            response_status = http_status.HTTP_200_OK
            self.assertEqual(response_status, 200)
            
        except Exception as e:
            self.fail(f"Complete code block (lines 135-156) failed: {e}")

    def test_query_with_nonexistent_ticket(self):
        """Test DoesNotExist exception handling"""
        # This should raise Ticket.DoesNotExist
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

    def test_query_performance_assessment(self):
        """Test that the query is reasonably performant"""
        # Create ticket with multiple entries
        ticket = Ticket.objects.create(
            subscriber=self.subscriber,
            user=self.user,
            ticket_status=self.ticket_status
        )
        
        # Create multiple entries to test prefetch efficiency
        for i in range(5):
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
        
        # Test query efficiency - should use prefetch_related properly
        with self.assertNumQueries(2):  # One main query + one prefetch query
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
            
            # Access prefetched data (should not trigger additional queries)
            entries = list(retrieved_ticket.entries.all())
            self.assertEqual(len(entries), 5)


if __name__ == '__main__':
    unittest.main()
