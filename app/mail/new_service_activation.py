from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# ... (previous tasks in the same file)

@shared_task
def send_new_service_activation_email(data):
    """
    A Celery task to send a new service activation notification.

    Args:
        data (dict): A dictionary containing subscriber and service details.
                     Example:
                     {
                         'recipient_email': 'notify@example.com',
                         'subscriber': {
                             'first_name': 'John',
                             'last_name': 'Doe',
                             'primary_email': 'john.doe@example.com',
                             'primary_phone': '555-123-4567',
                             'home': {
                                 'project': {'name': 'Verso Apartments'},
                                 'address': '123 Main St',
                                 'unit': 'A101'
                             },
                             'service_plan': {
                                 'description': '1Gbps Fiber Internet',
                                 'amount': 60.00
                             }
                         }
                     }
    """
    try:
        # This email seems to be a notification to an internal address.
        recipient_email = data.get('recipient_email')
        subject = "New Service Activation"

        if not recipient_email:
            print("Error: Recipient email for notification not found in data.")
            return

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/new_service_activation.html',
            {'data': data}
        )

        # Send the email.
        send_mail(
            subject=subject,
            message='',  # Plain-text version can be left empty.
            from_email=from_email,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"New service activation notice sent to {recipient_email}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending new service activation notice: {e}")
