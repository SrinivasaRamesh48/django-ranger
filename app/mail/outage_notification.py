from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# ... (previous tasks in the same file)

@shared_task
def send_outage_notification_email(data):
    """
    A Celery task to send a service outage notification.

    Args:
        data (dict): A dictionary containing the recipient's email, subject,
                     and the HTML body of the notification.
                     Example:
                     {
                         'recipient_email': 'subscriber@example.com',
                         'subject': 'Service Outage in Your Area',
                         'body': '<h3>Outage Alert</h3><p>We are aware of a service outage affecting your building...</p>'
                     }
    """
    try:
        recipient_email = data.get('recipient_email')
        subject = data.get('subject')
        body = data.get('body')

        if not all([recipient_email, subject, body]):
            print("Error: recipient_email, subject, and body are all required.")
            return

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/outage_notification.html',
            {'data': data}
        )

        # Send the email.
        send_mail(
            subject=subject,
            message='',  # Plain-text version, can be left empty if sending HTML.
            from_email=from_email,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Outage notification '{subject}' sent to {recipient_email}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending outage notification to {data.get('recipient_email', 'N/A')}: {e}")
