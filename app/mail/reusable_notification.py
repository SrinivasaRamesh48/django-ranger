from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# ... (previous tasks in the same file)

@shared_task
def send_reusable_notification_email(data):
    """
    A Celery task to send a simple, reusable test notification.

    Args:
        data (dict): A dictionary containing the recipient's email.
                     Example:
                     {
                         'recipient_email': 'test@example.com'
                     }
    """
    try:
        recipient_email = data.get('recipient_email')
        if not recipient_email:
            print("Error: Recipient email not found in data.")
            return

        # The subject of the email.
        subject = "Uprise Fiber - Test Email"

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/reusable_notification.html',
            {'data': data}
        )

        # Send the email.
        send_mail(
            subject=subject,
            message='Test',  # Plain-text version
            from_email=from_email,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Reusable notification (test email) sent to {recipient_email}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending reusable notification to {data.get('recipient_email', 'N/A')}: {e}")
