from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

@shared_task
def send_tickets_report_email(data):
    """
    A Celery task to compile and send the Tickets Report with attachments.

    Args:
        data (dict): A dictionary containing the report data, recipient,
                     and a list of attachment paths.
                     Example:
                     {
                         'recipient_email': 'report-recipient@example.com',
                         'start_date': '2025-06-18',
                         'end_date': '2025-06-25',
                         'attachments': [
                             '/path/to/report1.csv',
                             '/path/to/report2.pdf'
                         ],
                         'opened_tickets': [ ... ],
                         'closed_tickets': [ ... ]
                     }
    """
    try:
        recipient_email = data.get('recipient_email')
        attachments = data.get('attachments', [])

        if not recipient_email:
            print("Error: Recipient email not found in data.")
            return

        # The subject of the email.
        subject = "Uprise Fiber - Tickets Report"

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # Render the HTML content for the email from a Django template.
        html_body = render_to_string(
            'mail/tickets_report.html',
            {'data': data}
        )

        # Create an EmailMessage instance to handle the attachment(s).
        email = EmailMessage(
            subject=subject,
            body=html_body,
            from_email=from_email,
            to=[recipient_email],
        )
        email.content_subtype = "html"  # Set content type to HTML

        # Attach all files provided in the list.
        for attachment_path in attachments:
            try:
                email.attach_file(attachment_path)
            except FileNotFoundError:
                print(f"Attachment file not found at {attachment_path}, skipping.")

        # Send the email.
        email.send(fail_silently=False)

        print(f"Tickets Report sent to {recipient_email}")

    except Exception as e:
        # Log any other exceptions that occur.
        print(f"Error sending Tickets Report to {data.get('recipient_email', 'N/A')}: {e}")
