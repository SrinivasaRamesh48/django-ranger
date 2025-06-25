from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# ... (previous tasks in the same file)

@shared_task
def send_merchant_response_email(data):
    """
    A Celery task to send an email containing a pre-formatted merchant response.

    Args:
        data (dict): A dictionary containing the recipient's email and the
                     pre-formatted text content.
                     Example:
                     {
                         'recipient_email': 'admin@example.com',
                         'subject': 'Ranger - Merchant Response',
                         'contents': 'Transaction ID: 12345\nStatus: Approved\nAmount: 50.00'
                     }
    """
    try:
        recipient_email = data.get('recipient_email')
        contents = data.get('contents')
        subject = data.get('subject', 'Ranger - Merchant Response') # Default subject

        if not all([recipient_email, contents]):
            print("Error: recipient_email and contents are required.")
            return

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/merchant_response.html',
            {'data': data}
        )

        # Send the email.
        send_mail(
            subject=subject,
            message=contents,  # Use raw contents as the plain-text fallback
            from_email=from_email,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Merchant response email sent to {recipient_email}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending merchant response email to {data.get('recipient_email', 'N/A')}: {e}")
