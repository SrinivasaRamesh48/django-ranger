
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

# ... (previous tasks in the same file)

@shared_task
def send_payment_processed_email(data):
    """
    A Celery task to send a payment processed confirmation email.

    This task takes payment data, renders an HTML receipt, and sends it
    to the subscriber.

    Args:
        data (dict): A dictionary containing payment and subscriber details.
                     Example:
                     {
                         'subscriber': {
                            'first_name': 'John',
                            'email': 'john.doe@example.com'
                         },
                         'payment_amount': 50.00,
                     }
    """
    try:
        subscriber_email = data.get('subscriber', {}).get('email')
        if not subscriber_email:
            print("Error: Subscriber email not found in data.")
            return

        # The subject of the email.
        subject = "Uprise Fiber - Payment Processed"

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # The recipient's email address.
        recipient_list = [subscriber_email]

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/payment_processed.html',
            {'data': data}
        )

        # Send the email.
        send_mail(
            subject,
            '',  # Plain text message is empty as we send HTML.
            from_email,
            recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Payment processed notice sent to {subscriber_email}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending payment processed notice: {e}")

