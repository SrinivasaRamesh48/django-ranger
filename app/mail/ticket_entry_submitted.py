from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


@shared_task
def send_ticket_entry_submitted_email(data):
    """
    A Celery task to send a notification when a new ticket entry is submitted.

    Args:
        data (dict): A dictionary containing the details of the ticket entry.
                     Example:
                     {
                         'recipient_email': 'support-manager@example.com',
                         'ticket_entry_id': 789,
                         'ticket_id': 456,
                         'status': 'In Progress',
                         'category': 'Connectivity',
                         'technician': 'Tech Jane',
                         'subscriber_id': 123,
                         'subscriber': 'John Doe',
                         'email': 'john.doe@example.com',
                         'phone': '555-123-4567',
                         'project': 'Verso Apartments',
                         'address': '123 Main St',
                         'unit': 'A101',
                         'notes': 'Checked signal strength, appears to be a line issue.'
                     }
    """
    try:
        # This email seems to be a notification to an internal address.
        recipient_email = data.get('recipient_email')
        subject = "Ticket Entry Submitted from Ranger"

        if not recipient_email:
            print("Error: Recipient email for notification not found in data.")
            return

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/ticket_entry_submitted.html',
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
        print(f"Ticket entry submitted notice sent to {recipient_email}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending ticket entry submitted notice: {e}")
