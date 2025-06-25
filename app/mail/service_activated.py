from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# ... (previous tasks in the same file)

@shared_task
def send_service_activated_email(data):
    """
    A Celery task to send a "Welcome" email when a service is activated.

    Args:
        data (dict): A dictionary containing subscriber information.
                     Example:
                     {
                         'subscriber': {
                             'first_name': 'Jane',
                             'email': 'jane.doe@example.com'
                         }
                     }
    """
    try:
        subscriber_email = data.get('subscriber', {}).get('email')
        if not subscriber_email:
            print("Error: Subscriber email not found in data.")
            return

        # The subject of the email.
        subject = "Welcome to Uprise Fiber!"

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # The recipient's email address.
        recipient_list = [subscriber_email]

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/service_activated.html',
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
        print(f"Service activated welcome email sent to {subscriber_email}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending service activated email: {e}")
