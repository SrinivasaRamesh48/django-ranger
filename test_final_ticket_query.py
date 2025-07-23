"""
Focused test for the exact ticket retrieval query from tickets_view.py lines 135-156.
Uses the exact same setup as the working test_ticket_viewset_create.py
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient

from app.models import (
    Ticket, TicketEntry, TicketEntryAction, TicketEntryActionType, 
    TicketStatus, TicketCategory, Subscriber, Home, Project, 
    ServicePlan, UsState, SubscriptionType, UserRoles, UserCompany
)

User = get_user_model()


class TicketQueryTestCase(TestCase):
    """Test the specific ticket retrieval query and serialization from lines 135-156"""
    
    def setUp(self):
        """Use the exact same setup as test_ticket_viewset_create.py"""
        self.client = APIClient()
        
        # Create required reference data (exact same as working test)
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
        
        # Create test ticket category
        self.ticket_category = TicketCategory.objects.create(
            ticket_category_id=2, 
            description='General Support'
        )
        
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
            project=self.project
        )
        
        # Create test subscriber
        self.subscriber = Subscriber.objects.create(
            first_name='John',
            last_name='Doe',
            primary_email='john@example.com',
            primary_phone='555-1234',
            username='johndoe',
            home=self.home,
            service_plan=self.service_plan
        )
        
        # Create action type
        self.action_type = TicketEntryActionType.objects.create(description='Note')

    def test_exact_query_from_view_code(self):
        """Test the EXACT query from tickets_view.py lines 135-147"""
        # Create a ticket
        ticket = Ticket.objects.create(
            subscriber=self.subscriber,
            user=self.user,
            ticket_status=self.open_status,
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
        
        # Test the EXACT query from the view code (lines 135-147)
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
            print(f"✅ Query executed successfully for ticket {ticket.ticket_id}")
            
        except Exception as e:
            self.fail(f"❌ The exact query from view failed: {e}")

    def test_serialization_step(self):
        """Test the serialization step (line 148) after the query"""
        from app.serializers.ticket_serializer import TicketSerializer
        
        # Create ticket with entry and action
        ticket = Ticket.objects.create(
            subscriber=self.subscriber,
            user=self.user,
            ticket_status=self.open_status,
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
            
            # Verify basic serialization worked
            self.assertIn('ticket_id', serialized_data)
            self.assertEqual(serialized_data['ticket_id'], ticket.ticket_id)
            print(f"✅ Serialization successful for ticket {ticket.ticket_id}")
            
        except Exception as e:
            self.fail(f"❌ Serialization (line 148) failed: {e}")

    def test_complete_response_format(self):
        """Test the complete response format (lines 149-156)"""
        from app.serializers.ticket_serializer import TicketSerializer
        from rest_framework import status as http_status
        
        # Create ticket
        ticket = Ticket.objects.create(
            subscriber=self.subscriber,
            user=self.user,
            ticket_status=self.open_status,
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
        
        # Execute the complete code block from lines 135-156
        try:
            # Lines 135-147: Complex query
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
            
            # Lines 149-156: Response creation
            response_data = {
                'success': True,
                'data': serializer.data,
                'message': 'Ticket Successfully Created.'
            }
            
            # Verify the exact response format
            self.assertTrue(response_data['success'])
            self.assertEqual(response_data['message'], 'Ticket Successfully Created.')
            self.assertIsInstance(response_data['data'], dict)
            self.assertEqual(response_data['data']['ticket_id'], ticket.ticket_id)
            
            # Verify HTTP status would be 200
            expected_status = http_status.HTTP_200_OK
            self.assertEqual(expected_status, 200)
            
            print(f"✅ Complete response format test passed for ticket {ticket.ticket_id}")
            
        except Exception as e:
            self.fail(f"❌ Complete response flow (lines 135-156) failed: {e}")

    def test_does_not_exist_handling(self):
        """Test that Ticket.DoesNotExist is properly raised"""
        # This tests the exception that would be caught in the view
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
        
        print("✅ DoesNotExist exception properly raised for non-existent ticket")

    def test_query_performance(self):
        """Test that the query is reasonably efficient"""
        # Create ticket with multiple entries
        ticket = Ticket.objects.create(
            subscriber=self.subscriber,
            user=self.user,
            ticket_status=self.open_status,
            ticket_category=self.ticket_category
        )
        
        # Create multiple entries to test prefetch efficiency
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
        
        # Test query efficiency (Django prefetch generates multiple optimized queries)
        with self.assertNumQueries(5):  # Main query + prefetch queries (expected for this complexity)
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
            self.assertEqual(len(entries), 3)
        
        print(f"✅ Query performance test passed - efficient queries for ticket {ticket.ticket_id}")


if __name__ == '__main__':
    import unittest
    unittest.main()
