from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.db.models import Q
from app.models import Ticket, TicketEntry, TicketEntryAction, User, TicketStatus
from app.serializers import TicketSerializer, TicketEntrySerializer
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
        print("Creating ticket with data:", request.data)
        serializer = TicketSerializer(data=request.data)
        print("Creating ticket...")
        if serializer.is_valid():
            ticket = serializer.save()
            print(f"Ticket created: {ticket.ticket_id}")
            return Response({'success': True, 'data': serializer.data, 'message': 'Ticket created'})
        print(f"Ticket creation failed: {serializer.errors}")
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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
