from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# ... (previous tasks in the same file)

@shared_task
def send_technician_password_updated_email(data):
    """
    A Celery task to send a confirmation email after a technician's
    password has been updated.

    Args:
        data (dict): A dictionary containing the technician's details.
                     Example:
                     {
                         'recipient_email': 'technician@example.com',
                         'name': 'Tech Bob'
                     }
    """
    try:
        recipient_email = data.get('recipient_email')
        subject = "Ranger - Password Updated"

        if not recipient_email:
            print("Error: Recipient email for notification not found in data.")
            return

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/technician_password_updated.html',
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
        print(f"Technician password updated confirmation sent to {recipient_email}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending technician password updated email: {e}")