from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.db.models import Q
from app.models import Ticket, TicketEntry, TicketEntryAction, TicketEntryActionType, User, TicketStatus
from app.models import Subscriber
import random
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from app.serializers.ticket_serializer import TicketSerializer
from app.serializers.ticket_entry_serializer import TicketEntrySerializer
# from app.mail.ticket_closed_email import send_ticket_closed_email
# from app.mail.ticket_entry_email import send_ticket_entry_email

class TicketViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Ticket.objects.select_related(
            'ticket_category', 'ticket_status', 'user',
            'subscriber__home__project__circuit'
        ).all()
        serializer = TicketSerializer(queryset, many=True)
        return Response({'success': True, 'data': serializer.data, 'message': 'Tickets retrieved'})

    def retrieve(self, request, pk=None):
        ticket = get_object_or_404(Ticket.objects.select_related(
            'ticket_category', 'ticket_status', 'user',
            'subscriber__home__project__circuit'
        ), pk=pk)
        serializer = TicketSerializer(ticket)
        return Response({'success': True, 'data': serializer.data, 'message': 'Ticket retrieved'})

    def create(self, request):
        user = request.user
        input_data = request.data
        
        subscriber = None
        if input_data.get('new_subscriber') == True:
            # Check if email already exists
            if Subscriber.objects.filter(primary_email=input_data.get('email')).exists():
                response = {
                    'success': False,
                    'data': None,
                    'message': 'Failed to Create Subscriber.'
                }
                return Response(response, status=status.HTTP_200_OK)
            
            pool = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            random_password = ''.join(random.choices(pool, k=16))
            try:
                print(f"Creating subscriber with email: {input_data.get('email')}")
                subscriber = Subscriber.objects.create(
                    first_name=input_data.get('first_name'),
                    last_name=input_data.get('last_name'),
                    primary_email=input_data.get('email'),
                    primary_phone=input_data.get('phone'),
                    password=make_password(random_password)
                )
            except Exception as e:
                print(f"Error creating subscriber: {e}")
                subscriber = None
            
            if not subscriber:
                response = {
                    'success': False,
                    'data': None,
                    'message': 'Failed to Create Subscriber.'
                }
                return Response(response, status=status.HTTP_200_OK)
        
        # Create ticket if subscriber_id exists or subscriber was created
        if input_data.get('subscriber_id') or subscriber:
            # If using existing subscriber_id, validate it exists
            if input_data.get('subscriber_id') and not subscriber:
                try:
                    existing_subscriber = Subscriber.objects.get(subscriber_id=input_data.get('subscriber_id'))
                except Subscriber.DoesNotExist:
                    response = {
                        'success': False,
                        'data': None,
                        'message': 'Failed to Create Ticket.'
                    }
                    return Response(response, status=status.HTTP_200_OK)
            
            try:
                # Get the "Open" ticket status (default for new tickets)
                open_status = TicketStatus.objects.filter(description='Open').first()
                if not open_status:
                    # If no "Open" status exists, try to get the first available status
                    open_status = TicketStatus.objects.first()
                
                if not open_status:
                    ticket = None
                else:
                    ticket = Ticket.objects.create(
                        subscriber_id=input_data.get('subscriber_id') if input_data.get('subscriber_id') else subscriber.subscriber_id,
                        user_id=user.user_id,
                        ticket_status=open_status
                    )
            except Exception as e:
                ticket = None
            
            if ticket:
                try:
                    entry = TicketEntry.objects.create(
                        ticket_id=ticket.ticket_id,
                        user_id=user.user_id,
                        start_time=timezone.now(),
                        description=input_data.get('description', '')
                    )
                except Exception as e:
                    entry = None
                
                if entry:
                    try:
                        # Get the first action type (usually 'Note' or similar)
                        action_type = TicketEntryActionType.objects.first()
                        
                        action = TicketEntryAction.objects.create(
                            ticket_entry_id=entry.ticket_entry_id,
                            type=action_type
                        )
                    except Exception as e:
                        action = None
                    
                    if action:
                        try:
                            ticket = Ticket.objects.select_related(
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

                            serializer = TicketSerializer(ticket)
                            return Response({
                                'success': True,
                                'data': serializer.data,
                                'message': 'Ticket Successfully Created.'
                            }, status=status.HTTP_200_OK)
                        except Ticket.DoesNotExist:
                            return Response({
                                'success': False,
                                'message': 'Ticket not found.'
                            }, status=status.HTTP_404_NOT_FOUND)
                    else:
                        response = {
                            'success': False,
                            'data': None,
                            'message': 'Failed to Create Ticket.'
                        }
                else:
                    response = {
                        'success': False,
                        'data': None,
                        'message': 'Failed to Create Ticket.'
                    }
            else:
                response = {
                    'success': False,
                    'data': None,
                    'message': 'Failed to Create Ticket.'
                }
        else:
            response = {
                'success': False,
                'data': None,
                'message': 'Failed to Create Ticket.'
            }
        
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def update_ticket(self, request):
        ticket_id = request.data.get('id')
        ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
        serializer = TicketSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data, 'message': 'Ticket updated'})
        return Response({'success': False, 'errors': serializer.errors}, status=400)

    @action(detail=False, methods=['post'])
    def create_ticket_entry(self, request):
        serializer = TicketEntrySerializer(data=request.data)
        if serializer.is_valid():
            entry = serializer.save(user=request.user)
            # send_ticket_entry_email.delay(entry.id)
            return Response({'success': True, 'data': serializer.data, 'message': 'Entry created'})
        return Response({'success': False, 'errors': serializer.errors}, status=400)

    @action(detail=False, methods=['post'])
    def delete_ticket_entry(self, request):
        entry_id = request.data.get('id')
        try:
            entry = TicketEntry.objects.get(ticket_entry_id=entry_id)
            entry.delete()
            return Response({'success': True, 'message': 'Entry deleted'})
        except TicketEntry.DoesNotExist:
            return Response({'success': False, 'message': 'Entry not found'}, status=404)

    @action(detail=False, methods=['get'])
    def get_active_ticket(self, request):
        ticket = Ticket.objects.filter(ticket_status__description='Open').order_by('-opened_on').first()
        if ticket:
            serializer = TicketSerializer(ticket)
            return Response({'success': True, 'data': serializer.data})
        return Response({'success': False, 'message': 'No active ticket found'})

    @action(detail=True, methods=['post'])
    def add_entry(self, request, pk=None):
        ticket = get_object_or_404(Ticket, pk=pk)
        serializer = TicketEntrySerializer(data=request.data)
        if serializer.is_valid():
            entry = serializer.save(ticket=ticket, user=request.user)
            # send_ticket_entry_email.delay(entry.id)
            return Response({'success': True, 'data': serializer.data, 'message': 'Entry added'})
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def close_ticket(self, request, pk=None):
        ticket = get_object_or_404(Ticket, pk=pk)
        # Find the closed status or create it if it doesn't exist
        closed_status, _ = TicketStatus.objects.get_or_create(
            description='Closed',
            defaults={'description': 'Closed'}
        )
        ticket.ticket_status = closed_status
        ticket.closed_on = now()
        ticket.save()
        TicketEntry.objects.create(ticket=ticket, user=request.user, submitted=True, description="Ticket closed.")
        return Response({'success': True, 'message': 'Ticket closed'})

    @action(detail=True, methods=['post'])
    def reopen_ticket(self, request, pk=None):
        ticket = get_object_or_404(Ticket, pk=pk)
        # Find the reopened status or create it if it doesn't exist
        reopen_status, _ = TicketStatus.objects.get_or_create(
            description='Reopened',
            defaults={'description': 'Reopened'}
        )
        ticket.ticket_status = reopen_status
        ticket.closed_on = None
        ticket.save()
        TicketEntry.objects.create(ticket=ticket, user=request.user, submitted=True, description="Ticket reopened.")
        return Response({'success': True, 'message': 'Ticket reopened'})
        ticket.save()
        TicketEntry.objects.create(ticket=ticket, user=request.user, submitted=True, description="Ticket reopened.")
        return Response({'success': True, 'message': 'Ticket reopened'})

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        status_id = request.data.get('ticket_status_id')
        if not status_id:
            return Response({'success': False, 'message': 'ticket_status_id required'}, status=400)
        ticket = get_object_or_404(Ticket, pk=pk)
        ticket.ticket_status_id = status_id
        ticket.save()
        return Response({'success': True, 'message': 'Status updated'})

    @action(detail=False, methods=['get'], url_path='technician/(?P<technician_id>[^/.]+)')
    def technician_tickets(self, request, technician_id):
        tickets = Ticket.objects.filter(user_id=technician_id)
        serializer = TicketSerializer(tickets, many=True)
        return Response({'success': True, 'data': serializer.data})

    @action(detail=False, methods=['post'])
    def bulk_close(self, request):
        ticket_ids = request.data.get('ticket_ids', [])
        note = request.data.get('note', '')
        
        # Find the closed status or create it if it doesn't exist
        closed_status, _ = TicketStatus.objects.get_or_create(
            description='Closed',
            defaults={'description': 'Closed'}
        )
        
        updated = Ticket.objects.filter(ticket_id__in=ticket_ids).update(
            ticket_status=closed_status, 
            closed_on=now()
        )
        
        for tid in ticket_ids:
            TicketEntry.objects.create(ticket_id=tid, user=request.user, submitted=True, description=note)
        return Response({'success': True, 'message': f'{updated} tickets closed'})

    @action(detail=False, methods=['get'], url_path='chart/(?P<filter>[^/.]+)/(?P<timeframe>[^/.]+)')
    def tickets_chart_data(self, request, filter=None, timeframe=None):
        from datetime import timedelta
        from django.utils.timezone import now


        tf = int(timeframe)
        delta = timedelta(days=tf)
        start_date = now() - delta

        qs = Ticket.objects.filter(opened_on__gte=start_date)
        if filter == 'category':
            qs = qs.select_related('ticket_category')
        elif filter == 'circuit':
            qs = qs.select_related('subscriber__home__project__circuit')
        elif filter == 'project':
            qs = qs.select_related('subscriber__home__project')
        elif filter == 'technician':
            qs = qs.select_related('user')
        elif filter == 'status':
            qs = qs.select_related('ticket_status')
        else:
            qs = qs.select_related('ticket_category', 'ticket_status', 'user', 'subscriber__home__project__circuit')

        serializer = TicketSerializer(qs, many=True)
        return Response({'success': True, 'data': serializer.data})
