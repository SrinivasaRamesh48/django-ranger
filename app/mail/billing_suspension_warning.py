from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.dateparse import parse_date

# ... (previous tasks in the same file)

@shared_task
def send_billing_suspension_warning_email(data):
    """
    A Celery task to send a service suspension warning email.

    This task takes billing data, renders the HTML email from a template,
    and sends the warning email to the subscriber.

    Args:
        data (dict): A dictionary containing the statement and subscriber info.
                     Example:
                     {
                         'statement': {
                             'subscriber': {
                                 'first_name': 'Jane',
                                 'email': 'jane.doe@example.com'
                             },
                             'items': [
                                 # ... statement items
                             ],
                             'has_payments': False,
                             'balance': 225.00,
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
        subject = "Uprise Fiber - Suspension Warning"

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # The recipient's email address.
        recipient_list = [subscriber_email]

        # Ensure the due_date is a proper date object for template formatting.
        if 'due_date' in data['statement'] and isinstance(data['statement']['due_date'], str):
            data['statement']['due_date'] = parse_date(data['statement']['due_date'])

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/billing_suspension_warning.html',
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
        print(f"Suspension warning notice sent to {subscriber_email}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending suspension warning notice: {e}")

