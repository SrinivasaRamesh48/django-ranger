from datetime import timezone
from django.conf import settings
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from app.serializers import BulkEmailTemplateSerializer
from app.serializers import OutageSerializer
from app.serializers import BulkPhoneTemplateSerializer
from app.models import (
    Outage, Project, Alert, Home, OutageHomesEffected,BulkEmailTemplate, BulkPhoneTemplate,
    BulkMessageType, EmailLogItem, SubscriberEmailLog, SMSLogItem, SubscriberSMSLog
)
# --- Assumed Task & Email Imports ---
# These assume you have files for these classes/functions.
# from .tasks import send_bulk_email_task
# from .emails import PotentialOutageDetected

# --- Placeholder for external service/job logic ---
def send_potential_outage_email(email_data):
    # This would use your PotentialOutageDetected Mailable equivalent
    print("Sending potential outage email:", email_data)
    return True

# @shared_task
def send_bulk_sms_task(body, recipients):
    """
    A Celery task to send bulk SMS messages in the background.
    """
    print(f"Sending SMS via Celery: '{body}' to {len(recipients)} recipients.")
    # In a real implementation, you would use the Twilio client here.
    # from twilio.rest import Client
    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    # for recipient in recipients:
    #     client.messages.create(...)
    return True


class OutageViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing Outages. Corresponds to OutagesController.
    """
    queryset = Outage.objects.all()
    serializer_class = OutageSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'outage_id'

    def get_queryset(self):
        # Eager load related data to improve performance
        return Outage.objects.select_related('project', 'alert').prefetch_related(
            'effected', 'effected__home', 'effected__home__active_subscriber'
        )

    def list(self, request, *args, **kwargs):
        """Corresponds to the `index` method."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True, 'data': serializer.data, 'message': 'Outages Successfully Retrieved.'
        })

    def create(self, request, *args, **kwargs):
        """Corresponds to the `store` method."""
        user = request.user
        project_id = request.data.get('project_id')
        is_confirmed = request.data.get('confirmed', False)
        effected_home_ids = request.data.get('effectedHomeIds', [])
        
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return Response({'success': False, 'message': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            if is_confirmed:
                outage = Outage.objects.create(
                    project=project, confirmed=True, confirmed_at=timezone.now()
                )
                homes_to_link = [OutageHomesEffected(outage=outage, home_id=hid) for hid in effected_home_ids]
                OutageHomesEffected.objects.bulk_create(homes_to_link)
                Alert.objects.create(
                    alert_type_id=3, outage=outage, message=f"Outage detected at {project.name}.",
                    activated_by_id=1, updated_by_id=1
                )
            else:
                outage = Outage.objects.create(project=project, confirmed=False)
                Alert.objects.create(
                    alert_type_id=2, outage=outage, message=f"Possible Outage detected at {project.name} - Please confirm...",
                    activated_by_id=1, updated_by_id=1
                )
                # Send internal email notification
                email_data = {"project": project.name, "url": f"{settings.APP_URL}/admin"}
                send_potential_outage_email(email_data)
        
        return Response({'success': True, 'message': 'Outage Successfully Created.'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='outage-checkbox-nodes')
    def outage_checkbox_nodes(self, request):
        """Corresponds to `outage_checkbox_nodes`."""
        # This implementation closely mirrors the nested structure of the PHP version.
        checkbox_nodes = {}
        homes = Home.objects.select_related(
            'project', 'node', 'active_subscriber'
        ).order_by('project__name', 'node__hostname', 'node_switch_unit', 'node_port_num')

        for home in homes:
            p_id = home.project_id
            n_id = home.node.id if home.node else 0
            s_unit = f"Switch {home.node_switch_unit}" if home.node_switch_unit else "-"

            if p_id not in checkbox_nodes:
                checkbox_nodes[p_id] = {"value": f"project{p_id}", "label": home.project.name, "children": {}}
            
            if n_id not in checkbox_nodes[p_id]["children"]:
                 checkbox_nodes[p_id]["children"][n_id] = {"value": f"project{p_id}node{n_id}", "label": home.node.hostname if home.node else "-", "children": {}}

            if s_unit not in checkbox_nodes[p_id]["children"][n_id]["children"]:
                checkbox_nodes[p_id]["children"][n_id]["children"][s_unit] = {"value": f"project{p_id}node{n_id}switch{home.node_switch_unit}", "label": s_unit, "children": []}

            sub_name = f"{home.active_subscriber.first_name} {home.active_subscriber.last_name}" if home.active_subscriber else "-"
            home_label = f"Port: {home.node_port_num} Unit: {home.unit} Subscriber: {sub_name}"
            checkbox_nodes[p_id]["children"][n_id]["children"][s_unit]["children"].append({"value": home.home_id, "label": home_label})
        
        # Convert nested dictionaries to lists
        final_list = list(checkbox_nodes.values())
        for p in final_list:
            p['children'] = list(p['children'].values())
            for n in p['children']:
                n['children'] = list(n['children'].values())
        
        return Response({'success': bool(final_list), 'data': final_list})
        
    @action(detail=False, methods=['post'], url_path='confirm-outage-validity')
    def confirm_outage_validity(self, request):
        user = request.user
        is_valid = request.data.get('valid')
        outage_data = request.data.get('outage', {})
        outage_id = outage_data.get('outage_id')
        alert_id = outage_data.get('alert', {}).get('alert_id')
        effected_home_ids = request.data.get('effectedHomeIds', [])
        
        with transaction.atomic():
            if is_valid:
                Outage.objects.filter(pk=outage_id).update(confirmed=True, confirmed_at=timezone.now())
                Alert.objects.filter(pk=alert_id).update(alert_type_id=3, updated_by=user)
                homes_to_link = [OutageHomesEffected(outage_id=outage_id, home_id=hid) for hid in effected_home_ids]
                OutageHomesEffected.objects.bulk_create(homes_to_link)
            else:
                Outage.objects.filter(pk=outage_id).update(confirmed=False)
                Alert.objects.filter(pk=alert_id).update(active=False, deactivated_by=user)

        return Response({'success': True, 'message': 'Outage Successfully Updated.'})

    @action(detail=False, methods=['get'], url_path='outage-email-templates')
    def outage_email_templates(self, request):
        templates = BulkEmailTemplate.objects.filter(active=True)
        # In Django, you would likely have a foreign key on the template itself.
        # This is a direct translation of the logic.
        email_type = BulkMessageType.objects.get(pk=4)
        serializer = BulkEmailTemplateSerializer(templates, many=True)
        data = serializer.data
        for item in data:
            item['type'] = email_type.description
        return Response({'success': True, 'data': data})

    @action(detail=False, methods=['post'], url_path='outage-send-emails')
    def outage_send_emails(self, request):
        user = request.user
        data = request.data
        outage_id = data.get('outage_id')

        with transaction.atomic():
            log_item = EmailLogItem.objects.create(subject=data['subject'], body=data['body'], outage_id=outage_id)
            for item in data.get('homes', []):
                sub = item.get('home', {}).get('active_subscriber', {})
                if sub.get('primary_email'):
                    SubscriberEmailLog.objects.create(
                        subscriber_id=sub['subscriber_id'], sent_to=sub['primary_email'],
                        email_log_item_id=log_item.email_log_item_id, success=True
                    )
        
        # send_bulk_email_task.delay(data) # This would be the actual call
        print("Task would be dispatched here with data:", data)

        Outage.objects.filter(pk=outage_id).update(email_notices_sent=timezone.now())
        return Response({'success': True, 'message': 'Outage notification emails have been queued for sending.'})

    @action(detail=False, methods=['get'], url_path='outage-sms-templates')
    def outage_sms_templates(self, request):
        templates = BulkPhoneTemplate.objects.filter(active=True)
        sms_type = BulkMessageType.objects.get(pk=4)
        serializer = BulkPhoneTemplateSerializer(templates, many=True)
        data = serializer.data
        for item in data:
            item['type'] = sms_type.description
        return Response({'success': True, 'data': data})

    @action(detail=False, methods=['post'], url_path='outage-send-sms')
    def outage_send_sms(self, request):
        data = request.data
        outage_id = data.get('outage_id')
        recipients = []
        with transaction.atomic():
            log_item = SMSLogItem.objects.create(body=data['body'])
            for item in data.get('homes', []):
                sub = item.get('home', {}).get('active_subscriber', {})
                if sub.get('primary_phone'):
                    recipients.append({'binding_type': 'sms', 'address': sub['primary_phone']})
                    SubscriberSMSLog.objects.create(
                        subscriber_id=sub['subscriber_id'], sent_to=sub['primary_phone'],
                        sms_log_item_id=log_item.sms_log_item_id, success=True
                    )
        
        # Dispatch the task to the background queue.
        # The .delay() method is what makes it asynchronous.
        send_bulk_sms_task.delay(data.get('body'), recipients)
        
        Outage.objects.filter(pk=outage_id).update(phone_notices_sent=timezone.now())
        
        return Response({
            'success': True, 
            'message': 'Outage SMS notifications have been queued for sending.'
        })

    @action(detail=True, methods=['get'], url_path='outage-phone-message-set')
    def outage_phone_message_set(self, request, outage_id=None):
        Outage.objects.filter(pk=outage_id).update(phone_message_updated=timezone.now())
        return Response({'success': True})

    @action(detail=True, methods=['get'], url_path='outage-resolved')
    def outage_resolved(self, request, outage_id=None):
        user = request.user
        with transaction.atomic():
            outage = self.get_object()
            if outage.alert:
                outage.alert.active = False
                outage.alert.deactivated_by = user
                outage.alert.save()
            outage.resolved = timezone.now()
            outage.save()
        return Response({'success': True})
