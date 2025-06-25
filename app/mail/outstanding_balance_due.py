from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.dateparse import parse_date

# ... (previous tasks in the same file)

@shared_task
def send_outstanding_balance_due_email(data):
    """
    A Celery task to notify a subscriber about an outstanding balance.

    Args:
        data (dict): A dictionary containing subscriber and statement data.
                     Example:
                     {
                         'statement': {
                             'subscriber': {
                                 'first_name': 'John',
                                 'email': 'john.doe@example.com'
                             },
                             'balance': 95.00,
                             'due_date': '2025-06-24'
                         }
                     }
    """
    try:
        subscriber_email = data.get('statement', {}).get('subscriber', {}).get('email')
        if not subscriber_email:
            print("Error: Subscriber email not found in data.")
            return

        # The subject of the email.
        subject = "Uprise Fiber - Outstanding Balance Due"

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # The recipient's email address.
        recipient_list = [subscriber_email]
        
        # Ensure the due_date is a proper date object for template formatting.
        if 'due_date' in data['statement'] and isinstance(data['statement']['due_date'], str):
            data['statement']['due_date'] = parse_date(data['statement']['due_date'])

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/outstanding_balance_due.html',
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
        print(f"Outstanding balance due notice sent to {subscriber_email}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending outstanding balance due notice: {e}")
