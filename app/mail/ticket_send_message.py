from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# ... (previous tasks in the same file)

@shared_task
def send_ticket_send_message_email(data):
    """
    A Celery task to send a generic message related to a support ticket.

    Args:
        data (dict): A dictionary containing the message details.
                     Example:
                     {
                         'recipient_email': 'subscriber@example.com',
                         'values': 'This is a reply to your recent inquiry...'
                     }
    """
    try:
        recipient_email = data.get('recipient_email')
        message_content = data.get('values')

        if not all([recipient_email, message_content]):
            print("Error: recipient_email and values (message content) are required.")
            return

        subject = "Uprise Fiber - Ticket Message"
        from_email = settings.DEFAULT_FROM_EMAIL

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/ticket_send_message.html',
            {'data': data}
        )

        # Send the email.
        send_mail(
            subject=subject,
            message=message_content,  # Use raw content as the plain-text fallback
            from_email=from_email,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Ticket message sent to {recipient_email}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending ticket message: {e}")
