from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.db import transaction

from app.models import Subscriber, Ticket, TicketEntry, TicketEntryAction
from app.serializers import TicketSerializer  

class CreateTicketView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        subscriber = None

        try:
            with transaction.atomic():
                # Create subscriber if needed
                if data.get('new_subscriber') == True:
                    random_password = get_random_string(16)
                    subscriber = Subscriber.objects.create(
                        first_name=data.get('first_name'),
                        last_name=data.get('last_name'),
                        primary_email=data.get('email'),
                        primary_phone=data.get('phone'),
                        password=make_password(random_password),
                    )
                    if not subscriber:
                        return Response({
                            "success": False,
                            "data": None,
                            "message": "Failed to Create Subscriber."
                        })

                # Create Ticket
                if data.get('subscriber_id') or subscriber:
                    subscriber_id = data.get('subscriber_id') or getattr(subscriber, 'id', None)
                    ticket = Ticket.objects.create(
                        subscriber_id=subscriber_id,
                        user=user
                    )

                    if ticket:
                        entry = TicketEntry.objects.create(
                            ticket=ticket,
                            user=user,
                            start_time=timezone.now(),
                            description=""
                        )

                        if entry:
                            action = TicketEntryAction.objects.create(
                                ticket_entry=entry,
                                ticket_entry_action_type_id=1
                            )

                            if action:
                                # Load full ticket with relationships
                                active_ticket = Ticket.objects.select_related(
                                    'user', 'subscriber', 'subscriber__service_plan',
                                    'subscriber__home', 'subscriber__home__mac_address',
                                    'subscriber__home__node', 'subscriber__home__us_state',
                                    'subscriber__home__project', 'ticket_category',
                                    'ticket_status'
                                ).prefetch_related(
                                    'entries', 'entries__actions', 'entries__actions__type',
                                    'entries__dispatch_appointment',
                                    'entries__dispatch_appointment__type',
                                    'entries__dispatch_appointment__technician',
                                    'entries__dispatch_appointment__timeslot',
                                    'entries__dispatch_appointment__created_by',
                                    'entries__dispatch_appointment__canceled_by',
                                    'entries__service_change_schedule'
                                ).order_by('-ticket_status_id', '-opened_on').get(id=ticket.id)

                                # Add extra fields
                                ticket_data = TicketSerializer(active_ticket).data
                                ticket_data['minimize'] = False
                                ticket_data['close_ticket'] = False

                                return Response({
                                    "success": True,
                                    "data": ticket_data,
                                    "message": "Ticket Successfully Created."
                                })

            # If any creation failed
            return Response({
                "success": False,
                "data": None,
                "message": "Failed to Create Ticket."
            })
        except Exception as e:
            return Response({
                "success": False,
                "data": None,
                "message": f"Error occurred: {str(e)}"
            })
