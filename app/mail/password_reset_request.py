from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# ... (previous tasks in the same file)

@shared_task
def send_password_reset_request_email(data):
    """
    A Celery task to send a password reset request email.

    Args:
        data (dict): A dictionary containing subscriber information and the
                     password reset link.
                     Example:
                     {
                         'subscriber': {
                             'first_name': 'Jane',
                             'email': 'jane.doe@example.com'
                         },
                         'link': 'https://uprisefiber.com/password/reset/some_token'
                     }
    """
    try:
        subscriber_email = data.get('subscriber', {}).get('email')
        if not subscriber_email:
            print("Error: Subscriber email not found in data.")
            return

        # The subject of the email.
        subject = "Uprise Fiber - Password Reset Request"

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # The recipient's email address.
        recipient_list = [subscriber_email]

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/password_reset_request.html',
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
        print(f"Password reset request sent to {subscriber_email}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending password reset request: {e}")
