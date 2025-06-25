from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# ... (previous tasks in the same file)

@shared_task
def send_site_visit_closed_email(data):
    """
    A Celery task to send a notification that a site visit has been closed.

    Args:
        data (dict): A dictionary containing the details of the closed site visit.
                     Example:
                     {
                         'recipient_email': 'notify@example.com',
                         'site_visit_id': 123,
                         'ticket_id': 456,
                         'technician': 'Tech Bob',
                         'subscriber_id': 789,
                         'subscriber': 'Jane Doe',
                         'email': 'jane.doe@example.com',
                         'phone': '555-987-6543',
                         'project': 'Verso Apartments',
                         'address': '123 Main St',
                         'unit': 'B202',
                         'notes': 'Resolved connectivity issue by replacing the ethernet cable.'
                     }
    """
    try:
        # This email seems to be a notification to an internal address.
        recipient_email = data.get('recipient_email')
        subject = "Uprise Fiber - Site Visit Closed"

        if not recipient_email:
            print("Error: Recipient email for notification not found in data.")
            return

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/site_visit_closed.html',
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
        print(f"Site visit closed notice sent to {recipient_email}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending site visit closed notice: {e}")
