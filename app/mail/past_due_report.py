from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

# ... (previous tasks in the same file)

@shared_task
def send_past_due_report_email(data):
    """
    A Celery task to compile and send the Past Due Balances report.

    Args:
        data (dict): A dictionary containing the report data and recipient.
                     Example:
                     {
                         'recipient_email': 'report-recipient@example.com',
                         'date': '06/24/2025',
                         'past_due': [...], // List of all past due accounts
                         'deactivated': [...],
                         'suspended': [...],
                         'active': [...],
                         'deactivated_total': '1500.00',
                         'suspended_total': '3200.50',
                         'active_total': '5400.75'
                     }
    """
    try:
        recipient_email = data.get('recipient_email')
        report_date = data.get('date', timezone.now().strftime("%m/%d/%Y"))

        if not recipient_email:
            print("Error: Recipient email not found in data.")
            return

        # The subject of the email.
        subject = "Uprise Fiber - Past Due Balances Report"

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/past_due_balances_report.html',
            {
                'data': data,
            }
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
        print(f"Past Due Balances Report sent to {recipient_email}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending Past Due Balances Report to {data.get('recipient_email', 'N/A')}: {e}")
