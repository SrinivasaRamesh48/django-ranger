from celery import shared_task
from django.conf import settings
from app.mail.bulk_notification import send_bulk_notification_email


@shared_task(name="app.jobs.send_bulk_email")
def send_bulk_email_job(details):
    """
    A Celery task that dispatches multiple bulk emails, similar to the
    Laravel SendBulkEmail job. It iterates through a list of recipients
    and queues a separate `send_bulk_notification_email` task for each one.

    Args:
        details (dict): A dictionary containing the list of recipients and
                        the email subject and body.
                        Example:
                        {
                            'recipients': [
                                {'email': 'test1@example.com', 'first_name': 'John'},
                                {'email': 'test2@example.com', 'first_name': 'Jane'}
                            ],
                            'subject': 'An Important Update',
                            'body': '<p>This is the email content.</p>'
                        }
    """
    recipients = details.get('recipients', [])
    subject = details.get('subject')
    body = details.get('body')

    for recipient in recipients:
        recipient_email = recipient.get('email')
        if recipient_email:
            email_data = {
                'email': recipient_email,
                'first_name': recipient.get('first_name'),
                'last_name': recipient.get('last_name'),
                'subject': subject,
                'body': body
            }
            # Queue the single email sending task asynchronously
            send_bulk_notification_email.delay(email_data)
            print(f"Queued bulk email for {recipient_email}")

