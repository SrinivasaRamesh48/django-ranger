from app.models.bulk_message_type import BulkMessageType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db import transaction
from app.models import Home
from app.models import Subscriber, EmailLogItem, SubscriberEmailLog, SMSLogItem, SubscriberSMSLog,BulkEmailTemplate, BulkPhoneTemplate
from app.serializers.bulk_email_template_serializer import BulkEmailTemplateSerializer
from app.serializers.bulk_phone_template_serializer import BulkPhoneTemplateSerializer
from app.jobs.send_bulk_email import send_bulk_email_job  
from app.serializers.bulk_message_type_serializer import BulkMessageTypeSerializer
# from .twilio_client import send_bulk_sms
class BulkMessageView(APIView):
    def get_checkbox_nodes(self, label_key):
        """
        Builds the nested dictionary structure for the checkbox tree.

        Args:
            label_key (str): The attribute name on the ActiveSubscriber model
                             to use for the contact info (e.g., 'primary_email').
        """
        checkbox_nodes = {}
        all_ids = []

        # 1. Optimized Query: Fetch all necessary data in a single, efficient query.
        #    - We'll get all homes and filter for active subscribers in Python
        homes_queryset = Home.objects.select_related(
            'project__circuit',
            'node'
        ).prefetch_related(
            'subscribers'
        ).order_by(
            'project__circuit__circuit_id', 'project__project_id', 'node__node_id', 'node_switch_unit', 'node_port_num'
        )

        # 2. Process the queryset and build the nested structure.
        for home in homes_queryset:
            subscriber = home.active_subscriber()
            # Skip homes without active subscribers
            if not subscriber:
                continue
                
            project = home.project
            circuit = project.circuit if project else None
            node = home.node

            all_ids.append(subscriber.subscriber_id)

            circuit_id = circuit.circuit_id if circuit else 0
            circuit_dict = checkbox_nodes.setdefault(circuit_id, {
                "value": f"circuit{circuit_id}",
                "label": circuit.title if circuit and circuit.title else "Unassigned",
                "children": {}
            })

            project_id = project.project_id if project else 0
            project_dict = circuit_dict["children"].setdefault(project_id, {
                "value": f"circuit{circuit_id}project{project_id}",
                "label": project.name if project and project.name else "Unassigned",
                "children": {}
            })

            node_id = node.node_id if node else 0
            node_dict = project_dict["children"].setdefault(node_id, {
                "value": f"circuit{circuit_id}project{project_id}node{node_id}",
                "label": node.hostname if node and node.hostname else "Unassigned",
                "children": {}
            })

            switch_unit = home.node_switch_unit if home.node_switch_unit is not None else 0
            switch_value = f"circuit{circuit_id}project{project_id}node{node_id}switch{switch_unit}" if home.node_switch_unit is not None else f"unassigned-switch-{node_id}"
            switch_dict = node_dict["children"].setdefault(switch_unit, {
                "value": switch_value,
                "label": f"Switch {switch_unit}" if home.node_switch_unit is not None else "Unassigned",
                "children": []
            })

            # Use getattr for dynamic attribute access (email or phone)
            contact_info = getattr(subscriber, label_key, 'N/A') or 'N/A'

            home_node = {
                "value": subscriber.subscriber_id,
                "label": (
                    f"Port: {home.node_port_num or 'N/A'} "
                    f"Unit: {home.unit or 'N/A'} "
                    f"Subscriber: {subscriber.full_name} - {contact_info}"
                )
            }
            switch_dict["children"].append(home_node)

        # 3. Restructure the nested dictionaries into lists.
        final_data = list(checkbox_nodes.values())
        for circuit_item in final_data:
            circuit_item['children'] = list(circuit_item['children'].values())
            for project_item in circuit_item['children']:
                project_item['children'] = list(project_item['children'].values())
                for node_item in project_item['children']:
                    node_item['children'] = list(node_item['children'].values())

        # 4. Return the final data payload.
        return {
            'success': bool(final_data),
            'data': final_data,
            'all_ids': all_ids
        }



# API endpoint to get the checkbox node structure with subscriber emails.
class BulkMessageEmailNodesView(BulkMessageView):
    def get(self, request, *args, **kwargs):
        response_data = self.get_checkbox_nodes(label_key='primary_email')
        return Response(response_data, status=status.HTTP_200_OK)


# API endpoint to get the checkbox node structure with subscriber phone numbers.
class BulkMessagePhoneNodesView(BulkMessageView):

    def get(self, request, *args, **kwargs):
        response_data = self.get_checkbox_nodes(label_key='primary_phone')
        return Response(response_data, status=status.HTTP_200_OK)


class BulkMessageSendEmailsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        input_data = request.data

        subject = input_data.get('subject')
        body = input_data.get('body')
        subscriber_ids = input_data.get('subscriber_ids', [])
        bulk_type_id = input_data.get('bulk_message_type_id')

        email_log_item = EmailLogItem.objects.create(
            subject=subject,
            body=body,
            bulk_message_type_id=bulk_type_id
        )

        # Fix f-string syntax - can't use backslash in expression
        formatted_body = body.replace('\n', '<br>')
        email_body = f"<p>{formatted_body}</p>"
        recipients = []

        for subscriber_id in subscriber_ids:
            subscriber = get_object_or_404(Subscriber, pk=subscriber_id)

            if settings.ENVIRONMENT == 'production':
                if subscriber.primary_email and "@" in subscriber.primary_email and "." in subscriber.primary_email:
                    recipient = {
                        "first_name": subscriber.first_name,
                        "last_name": subscriber.last_name,
                        "email": subscriber.primary_email
                    }
            else:
                recipient = {
                    "first_name": "Test",
                    "last_name": "Test",
                    "email": user.email
                }

            if "email" in recipient:
                recipients.append(recipient)
                SubscriberEmailLog.objects.create(
                    subscriber=subscriber,
                    sent_to=recipient['email'],
                    email_log_item=email_log_item,
                    success=True
                )

        if settings.ENVIRONMENT == 'production':
            recipients.append({
                "first_name": "Uprise",
                "last_name": "Fiber",
                "email": "customerservice@uprisefiber.com"
            })

        send_bulk_email_job.delay({
            "subject": subject,
            "body": email_body,
            "recipients": recipients
        })

        return Response({
            'success': True,
            'message': 'Notifications sent'
        }, status=status.HTTP_200_OK)


class BulkMessageSendSMSView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        input_data = request.data

        body = input_data.get('body')
        subscriber_ids = input_data.get('subscriber_ids', [])
        bulk_type_id = input_data.get('bulk_message_type_id')

        sms_log_item = SMSLogItem.objects.create(
            body=body,
            bulk_message_type_id=bulk_type_id
        )

        recipients = []

        for subscriber_id in subscriber_ids:
            subscriber = get_object_or_404(Subscriber, pk=subscriber_id)

            if settings.ENVIRONMENT == 'production':
                if subscriber.primary_phone:
                    recipient = {
                        "binding_type": "sms",
                        "address": subscriber.primary_phone
                    }
            else:
                recipient = {
                    "binding_type": "sms",
                    "address": "5036864263"
                }

            if recipient.get("address"):
                recipients.append(recipient)
                SubscriberSMSLog.objects.create(
                    subscriber=subscriber,
                    sent_to=recipient["address"],
                    sms_log_item=sms_log_item,
                    success=True
                )

        # send_bulk_sms_task.delay(body, recipients)

        return Response({
            'success': True,
            'message': f'{len(subscriber_ids)} Message(s) Sent'
        }, status=status.HTTP_200_OK)


class BulkMessageSubscriberEmailLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        log_entries = SubscriberEmailLog.objects.select_related('email_log_item').filter(email_log_item_id=id)
        data = []
        for item in log_entries:
            subscriber = get_object_or_404(Subscriber, pk=item.subscriber_id)
            data.append({
                "subscriber_id": subscriber.pk,
                "subscriber_name": f"{subscriber.first_name} {subscriber.last_name}",
                "sent_to": item.sent_to,
                "success": item.success,
                "email_log_item_id": item.email_log_item_id,
                "created_at": item.created_at,
               
            })
        return Response({'data': data}, status=status.HTTP_200_OK)

class BulkMessageSubscriberSMSLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        log_entries = SubscriberSMSLog.objects.select_related('sms_log_item').filter(sms_log_item_id=id)
        data = []
        for item in log_entries:
            subscriber = get_object_or_404(Subscriber, pk=item.subscriber_id)
            data.append({
                "subscriber_id": subscriber.pk,
                "subscriber_name": f"{subscriber.first_name} {subscriber.last_name}",
                "sent_to": item.sent_to,
                "success": item.success,
                "sms_log_item_id": item.sms_log_item_id,
                "created_at": item.created_at,
                
            })
        return Response({'data': data}, status=status.HTTP_200_OK)


class BulkMessageTypesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        types = BulkMessageType.objects.all()
        serializer = BulkMessageTypeSerializer(types, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class BulkMessageNewEmailTemplateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        input_data = request.data
        template = BulkEmailTemplate.objects.create(
            bulk_message_type_id=input_data['bulk_message_type_id'],
            description=input_data['description'],
            subject=input_data['subject'],
            body=input_data['body'],
        )
        success = template is not None
        return Response({
            'success': success,
            'message': 'Template Successfully Added.' if success else 'Failed to Add Template.'
        }, status=status.HTTP_200_OK)


class BulkMessageNewPhoneTemplateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        input_data = request.data
        template = BulkPhoneTemplate.objects.create(
            bulk_message_type_id=input_data['bulk_message_type_id'],
            description=input_data['description'],
            body=input_data['body'],
        )
        success = template is not None
        return Response({
            'success': success,
            'message': 'Template Successfully Added.' if success else 'Failed to Add Template.'
        }, status=status.HTTP_200_OK)


class BulkMessageEditEmailTemplateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        data = request.data
        updated = BulkEmailTemplate.objects.filter(
            outage_email_template_id=data['selectedTemplateId']
        ).update(
            bulk_message_type_id=data['bulk_message_type_id'],
            description=data['description'],
            subject=data['subject'],
            body=data['body']
        )
        return Response({'success': bool(updated)}, status=status.HTTP_200_OK)


class BulkMessageEditPhoneTemplateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        data = request.data
        updated = BulkPhoneTemplate.objects.filter(
            outage_phone_template_id=data['selectedTemplateId']
        ).update(
            bulk_message_type_id=data['bulk_message_type_id'],
            description=data['description'],
            body=data['body']
        )
        return Response({'success': bool(updated)}, status=status.HTTP_200_OK)


class BulkMessageRemoveEmailTemplateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        updated = BulkEmailTemplate.objects.filter(
            outage_email_template_id=id
        ).update(active=False)
        return Response({'success': bool(updated)}, status=status.HTTP_200_OK)


class BulkMessageRemovePhoneTemplateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        updated = BulkPhoneTemplate.objects.filter(
            outage_phone_template_id=id
        ).update(active=False)
        return Response({'success': bool(updated)}, status=status.HTTP_200_OK)



class BulkMessageEmailTemplateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        template = BulkEmailTemplate.objects.filter(
            outage_email_template_id=id
        )
        serializer = BulkEmailTemplateSerializer(template, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class BulkMessagePhoneTemplateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        template = BulkPhoneTemplate.objects.filter(
            outage_phone_template_id=id
        )
        serializer = BulkPhoneTemplateSerializer(template, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    