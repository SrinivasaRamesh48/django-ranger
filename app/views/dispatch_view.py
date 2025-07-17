# # app/views.py

# import datetime
# from django.conf import settings
# from django.db import transaction
# from django.utils import timezone
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# # Assuming a utility file for external service calls and helpers
# from . import services
# from .serializers import DispatchAppointmentSerializer, DispatchAppointmentTimeslotSerializer, DispatchAppointmentTypeSerializer

# # Import models and mailers as requested
# from app.models import (
#     DispatchAppointment, DispatchAppointmentTimeslot, DispatchAppointmentType,
#     MacAddress, Subscriber, Home, Ticket, TicketEntry, TicketEntryAction,
#     ServiceChangeSchedule, ServicePlan
# )
# from app.mail import ServiceActivated, SiteVisitClosed

# class DispatchAppointmentListView(APIView):
#     """
#     Handles fetching all dispatch appointments.
#     """
#     def get(self, request):
#         """
#         Retrieves a list of all dispatch appointments with related data.
#         Equivalent to the index() method.
#         """
#         appointments = DispatchAppointment.objects.select_related(
#             'type', 'technician', 'timeslot', 'created_by', 'canceled_by', 'ticket',
#             'ticket__ticket_category', 'ticket__ticket_status', 'ticket__user',
#             'ticket__subscriber__home__node', 'ticket__subscriber__home__us_state',
#             'ticket__subscriber__home__project'
#         ).prefetch_related('ticket__entries').all()

#         serializer = DispatchAppointmentSerializer(appointments, many=True)
#         response_data = {
#             'success': True,
#             'data': serializer.data,
#             'message': 'Appointments Successfully Retrieved.'
#         }
#         return Response(response_data, status=status.HTTP_200_OK)

# class DispatchAppointmentTimeslotListView(APIView):
#     """
#     Provides a list of active dispatch appointment timeslots.
#     """
#     def get(self, request):
#         timeslots = DispatchAppointmentTimeslot.objects.filter(active=True)
#         serializer = DispatchAppointmentTimeslotSerializer(timeslots, many=True)
#         return Response(serializer.data)

# class DispatchAppointmentTypeListView(APIView):
#     """
#     Provides a list of all dispatch appointment types.
#     """
#     def get(self, request):
#         types = DispatchAppointmentType.objects.all()
#         serializer = DispatchAppointmentTypeSerializer(types, many=True)
#         return Response(serializer.data)


# class CloseDispatchAppointmentView(APIView):
#     """
#     Handles the logic for closing a dispatch appointment.
#     Equivalent to the close_dispatch_appointment() method.
#     """
#     @transaction.atomic
#     def post(self, request):
#         user = request.user
#         data = request.data
#         appointment_data = data.get('appointment', {})
#         ticket_data = appointment_data.get('ticket', {})
#         subscriber_data = ticket_data.get('subscriber', {})
#         home_data = subscriber_data.get('home', {})

#         # --- Service Activation (if appointment type is 1) ---
#         if appointment_data.get('dispatch_appointment_type_id') == 1:
#             self._handle_service_activation(data, user, appointment_data)

#         # --- Home Wiring Certification ---
#         wiring_certified = data.get('wiring_certified', [0])[0] == 1
#         if wiring_certified:
#             Home.objects.filter(home_id=home_data['home_id']).update(
#                 wiring_certified_on=timezone.now(),
#                 wiring_certified_by=user
#             )

#         # --- Update Appointment and Ticket Status ---
#         wiring_repaired = data.get('wiring_repaired', [0])[0] == 1
#         self._update_entities(appointment_data, ticket_data, data, user, wiring_certified, wiring_repaired)

#         # --- Send Closure Notification Email ---
#         self._send_closure_email(data, user)

#         response = {
#             'success': True,
#             'message': 'Appointment Successfully Closed.'
#         }
#         return Response(response, status=status.HTTP_200_OK)

#     def _handle_service_activation(self, data, user, appointment_data):
#         """
#         Private helper to encapsulate service activation logic.
#         """
#         subscriber_data = appointment_data.get('ticket', {}).get('subscriber', {})
#         home_data = subscriber_data.get('home', {})

#         # Create CPE ID and update/create MacAddress
#         cpe_id = f"{data['mac_address'].replace(':', '')[:6]}-ACRouter-{data['serial_number']}"
#         MacAddress.objects.filter(home_id=home_data['home_id']).update(home_id=None)
        
#         mac = MacAddress.objects.create(
#             address=data['mac_address'],
#             home_id=home_data['home_id'],
#             cpe_id=cpe_id,
#             cpe_serial_number=data['serial_number'],
#             default_ssid=services.encrypt_string(f"Uprise-Fiber-{home_data['unit']}"),
#             default_passkey=services.encrypt_string(services.generate_random_password())
#         )
#         Home.objects.filter(home_id=home_data['home_id']).update(mac_address_id=mac.mac_address_id)

#         # Check for pending service changes
#         activation_check = ServiceChangeSchedule.objects.filter(
#             subscriber_id=subscriber_data['subscriber_id'],
#             processed__isnull=True,
#             canceled=False
#         ).first()

#         if activation_check:
#             # External service calls are moved to a dedicated services module
#             services.activate_service(data['mac_address'], home_data['node']['ip_address'])
#             services.enable_cpe_radio(cpe_id)
#             services.reset_cpe_credentials(cpe_id, activation_check.ssid_1, activation_check.passkey_1, activation_check.ssid_2, activation_check.passkey_2)

#             Subscriber.objects.filter(subscriber_id=subscriber_data['subscriber_id']).update(
#                 service_plan_id=activation_check.service_plan_id,
#                 service_activated_on=timezone.now(),
#                 service_deactivated_on=None
#             )
            
#             activation_check.processed = timezone.now()
#             activation_check.save()
            
#             service_plan = ServicePlan.objects.get(service_plan_id=activation_check.service_plan_id)
#             project = home_data.get('project', {})
#             if not service_plan.bulk:
#                  services.create_initial_billing_statement(subscriber_data['subscriber_id'], service_plan, project.get('free_month'), project.get('free_month_2'))

#             # Send Service Activated Email
#             subscriber_instance = Subscriber.objects.get(subscriber_id=subscriber_data['subscriber_id'])
#             email_data = {"subscriber": subscriber_instance}
#             recipient = subscriber_data['primary_email'] if not settings.DEBUG else user.email
#             if recipient:
#                 ServiceActivated(email_data).send(to=[recipient])


#     def _update_entities(self, appointment_data, ticket_data, data, user, wiring_certified, wiring_repaired):
#         """
#         Private helper to update database records for appointment, ticket, and entries.
#         """
#         DispatchAppointment.objects.filter(dispatch_appointment_id=appointment_data['dispatch_appointment_id']).update(
#             completion_notes=data["completion_notes"],
#             completed_on=timezone.now(),
#             wiring_certified=wiring_certified,
#             wiring_repaired=wiring_repaired,
#         )

#         Ticket.objects.filter(ticket_id=ticket_data['ticket_id']).update(
#             ticket_status_id=1,  # Assuming 1 is 'Closed'
#             closed_on=timezone.now()
#         )

#         entry = TicketEntry.objects.create(
#             ticket_id=ticket_data['ticket_id'],
#             user=user,
#             start_time=timezone.now(),
#             end_time=timezone.now(),
#             submitted=True,
#             description="Dispatch Appointment Complete, Ticket Closed."
#         )

#         TicketEntryAction.objects.create(
#             ticket_entry=entry,
#             ticket_entry_action_type_id=2  # Assuming 2 corresponds to a closing action
#         )

#     def _send_closure_email(self, data, user):
#         """
#         Private helper to build context and send the final site visit closure email.
#         """
#         appointment_data = data.get('appointment', {})
#         ticket_data = appointment_data.get('ticket', {})
#         subscriber_data = ticket_data.get('subscriber', {})
#         home_data = subscriber_data.get('home', {})
#         project_data = home_data.get('project', {})

#         email_data = {
#             "site_visit_id": appointment_data.get('dispatch_appointment_id'),
#             "ticket_id": ticket_data.get('ticket_id'),
#             "technician": user.get_full_name() or user.username,
#             "subscriber_id": subscriber_data.get('subscriber_id'),
#             "subscriber": f"{subscriber_data.get('first_name')} {subscriber_data.get('last_name')}",
#             "email":  subscriber_data.get('primary_email'),
#             "phone": subscriber_data.get('primary_phone'),
#             "project": project_data.get('name'),
#             "address": home_data.get('address'),
#             "unit": home_data.get('unit'),
#             "notes": data.get('completion_notes'),
#             "ki": project_data.get('builder_id') == 3,
#             "wiring_certified": "Yes" if data.get('wiring_certified', [0])[0] == 1 else "No",
#             "wiring_repaired": "Yes" if data.get('wiring_repaired', [0])[0] == 1 else "No",
#         }
        
#         recipients = ["jchapman@uprisefiber.com", "amccall@uprisefiber.com"] if not settings.DEBUG else [user.email]
#         SiteVisitClosed(email_data).send(to=recipients)