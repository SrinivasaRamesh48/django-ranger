from ranger.celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# The soft_time_limit argument is the Celery equivalent of Laravel's $timeout property.
# It will raise an exception if the task runs longer than the specified time in seconds.
@shared_task(soft_time_limit=14400) # 14400 seconds = 4 hours
def send_bulk_email_task(details):
    """
    A Celery task that sends bulk emails, equivalent to the SendBulkEmail job.

    Args:
        details (dict): A dictionary containing the email details, including
                        'recipients', 'subject', and 'body'.
    """
    recipients = details.get('recipients', [])
    subject = details.get('subject', 'A Notification from Uprise Fiber')
    body_content = details.get('body', '')

    for recipient in recipients:
        email = recipient.get('email')
        first_name = recipient.get('first_name')
        last_name = recipient.get('last_name')

        if not email:
            continue

        # Prepare the context for the email template.
        # This is equivalent to the data passed to the BulkNotification Mailable.
        context = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'body': body_content
        }

        # Render the HTML body from a template.
        html_message = render_to_string('mail/bulk-notification.html', context)
        # Use the raw body as a plain-text fallback.
        plain_message = body_content

        try:
            # Send the email using Django's core mail utility.
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )
            print(f"Bulk notification email queued for {email}")
        except Exception as e:
            # It's good practice to log any failed email attempts.
            print(f"Failed to send bulk notification to {email}: {e}")

# ==============================================================================
# Example Email Template (templates/mail/bulk-notification.html)
# ==============================================================================
"""
<!DOCTYPE html>
<html>
<head>
    <title>{{ subject }}</title>
</head>
<body>
    <p>Hi {{ first_name }} {{ last_name }},</p>
    
    <!-- The |safe filter allows rendering the HTML content from the body -->
    <div>{{ body|safe }}</div>

    <p>Thank you,</p>
    <p>The Uprise Fiber Team</p>
</body>
</html>
"""

# ==============================================================================
# Example Usage (from a views.py or another task)
# ==============================================================================
"""
# from .tasks import send_bulk_email_task # Import the task

def some_view_that_triggers_the_bulk_email(request):
    # 1. Gather the data for the bulk email job
    email_details = {
        "subject": "Important Service Update",
        "body": "<p>We will be performing scheduled maintenance tonight.</p>",
        "recipients": [
            {"first_name": "John", "last_name": "Doe", "email": "john@example.com"},
            {"first_name": "Jane", "last_name": "Smith", "email": "jane@example.com"},
        ]
    }
    
    # 2. Call the task with .delay() to run it in the background
    send_bulk_email_task.delay(email_details)
    
    # 3. Return a response to the user immediately
    return Response({"status": "Bulk email job has been dispatched."})
"""