from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# ... (previous tasks in the same file)

@shared_task
def send_maintenance_notification_email(data):
    """
    A Celery task to send a network maintenance notification.

    Args:
        data (dict): A dictionary containing subscriber information and
                     dynamic content for the notification.
                     Example:
                     {
                         'subscriber': {
                             'first_name': 'John',
                             'email': 'john.doe@example.com'
                         },
                         'subject': 'Uprise Fiber - Network Maintenance - Wednesday 5/19 12:00PM',
                         'maintenance_time': 'Wednesday, May 19th at 12:00pm',
                         'duration': 'up to 2 hours, lasting until 2:00pm',
                         'location': 'at Verso Apartments'
                     }
    """
    try:
        subscriber_email = data.get('subscriber', {}).get('email')
        subject = data.get('subject', 'Network Maintenance Notification')

        if not subscriber_email:
            print("Error: Subscriber email not found in data.")
            return

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/maintenance_notification.html',
            {'data': data}
        )

        # Send the email.
        send_mail(
            subject=subject,
            message='',  # Plain-text version can be left empty.
            from_email=from_email,
            recipient_list=[subscriber_email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Maintenance notification sent to {subscriber_email}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending maintenance notification to {data.get('subscriber', {}).get('email', 'N/A')}: {e}")
