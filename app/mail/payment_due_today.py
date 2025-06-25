from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.dateparse import parse_date

# ... (previous tasks in the same file)

@shared_task
def send_payment_due_today_email(data):
    """
    A Celery task to send a "payment due today" reminder email.

    Args:
        data (dict): A dictionary containing subscriber and statement data.
                     Example:
                     {
                         'subscriber': {
                             'first_name': 'John',
                             'email': 'john.doe@example.com'
                         },
                         'statement': {
                             'balance': 75.00,
                             'items': [
                                 # ... statement items
                             ],
                             'has_payments': True,
                             'due_date': '2025-06-25'
                         }
                     }
    """
    try:
        subscriber_email = data.get('subscriber', {}).get('email')
        if not subscriber_email:
            print("Error: Subscriber email not found in data.")
            return

        # The subject of the email.
        subject = "Uprise Fiber - Payment Due"

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # The recipient's email address.
        recipient_list = [subscriber_email]

        # Ensure the due_date is a proper date object for template formatting.
        if 'statement' in data and 'due_date' in data['statement'] and isinstance(data['statement']['due_date'], str):
            data['statement']['due_date'] = parse_date(data['statement']['due_date'])

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/payment_due_today.html',
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
        print(f"Payment due today reminder sent to {subscriber_email}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending payment due today reminder: {e}")
