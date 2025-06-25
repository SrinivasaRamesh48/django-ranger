from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

# ... (previous tasks in the same file)

@shared_task
def send_keystone_report_email(data):
    """
    A Celery task to compile and send the Keystone Report email.

    Args:
        data (dict): A dictionary containing the report data and recipient.
                     Example:
                     {
                         'recipient_email': 'report-recipient@example.com',
                         'appointments': [
                             {'date': '06/24/2025', 'timeslot': '9am', ...},
                             ...
                         ],
                         'homes': [
                             {'unit': 'A101', 'subscriber': 'John Doe', ...},
                             ...
                         ]
                     }
    """
    try:
        recipient_email = data.get('recipient_email')
        if not recipient_email:
            print("Error: Recipient email not found in data.")
            return

        # Get the current date in m/d format.
        current_date_str = timezone.now().strftime("%m/%d")

        # The subject of the email.
        subject = f"Keystone Report - {current_date_str}"

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/keystone_report.html',
            {
                'data': data,
                'date': current_date_str
            }
        )

        # Send the email.
        send_mail(
            subject=subject,
            message='',  # Plain-text version, can be left empty.
            from_email=from_email,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"Keystone Report sent to {recipient_email}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending Keystone Report to {data.get('recipient_email', 'N/A')}: {e}")

