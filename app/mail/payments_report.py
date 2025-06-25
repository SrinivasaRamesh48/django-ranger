from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

# ... (previous tasks in the same file)

@shared_task
def send_payments_report_email(data):
    """
    A Celery task to compile and send the Payments Report email for the previous month.

    Args:
        data (dict): A dictionary containing the report data and recipient.
                     Example:
                     {
                         'recipient_email': 'report-recipient@example.com',
                         'start_date': '2025-05-01',
                         'end_date': '2025-05-31',
                         'optin_summary': {
                             'payments': '5000.00',
                             'fees': '150.00',
                             'net': '4850.00'
                         },
                         'optin_projects': [
                             {'name': 'Project A', 'address': '123 Alpha St', 'city': 'Metro', 'payments': '3000.00'},
                             {'name': 'Project B', 'address': '456 Beta Ave', 'city': 'Cityburg', 'payments': '2000.00'}
                         ]
                     }
    """
    try:
        recipient_email = data.get('recipient_email')
        if not recipient_email:
            print("Error: Recipient email not found in data.")
            return

        # Calculate the name of last month for the subject.
        today = timezone.now().date()
        first_day_of_current_month = today.replace(day=1)
        last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
        report_month_str = last_day_of_last_month.strftime("%B %Y")

        # The subject of the email.
        subject = f"Uprise Fiber Payments Report - {report_month_str}"

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/payments_report.html',
            {
                'data': data,
                'date': report_month_str
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
        print(f"Payments Report sent to {recipient_email}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending Payments Report to {data.get('recipient_email', 'N/A')}: {e}")
