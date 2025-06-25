from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

@shared_task
def send_billing_notice_email(subscriber_data):
    """
    A Celery task to send a billing notice email.

    This task takes subscriber data as an argument, renders the HTML email
    content from a Django template, and sends the email.

    Args:
        subscriber_data (dict): A dictionary containing the subscriber's
                                information, such as 'first_name' and 'email'.
                                Example:
                                {
                                    'first_name': 'John',
                                    'email': 'john.doe@example.com'
                                }
    """
    try:
    
        subject = "Uprise Fiber - Billing Notice"

        # The sender's email address, usually configured in settings.py.
        from_email = settings.DEFAULT_FROM_EMAIL

        # The recipient's email address from the subscriber data.
        recipient_list = [subscriber_data.get('email')]

        # Render the HTML content for the email from a Django template.
        # We pass the subscriber_data to the template context.
        html_message = render_to_string(
            'mail/billing_notice.html',
            {'data': {'subscriber': subscriber_data}}
        )

        # Send the email.
        # The plain text message is left empty as we are sending an HTML email.
        send_mail(
            subject,
            '',  # Plain text message (optional)
            from_email,
            recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        # You can add logging here to confirm the email was sent.
        print(f"Billing notice sent to {subscriber_data.get('email')}")

    except Exception as e:
        print(f"Error sending billing notice to {subscriber_data.get('email')}: {e}")
