from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

# ... (previous tasks in the same file)

@shared_task
def send_leasing_referrals_report_email(data):
    """
    A Celery task to compile and send the Leasing Referrals report email.

    Args:
        data (dict): A dictionary containing the report data and recipient.
                     Example:
                     {
                         'recipient_email': 'report-recipient@example.com',
                         'date': '06/24/2025',
                         'projects': [
                             {
                                 'name': 'Project Alpha',
                                 'staff': [
                                     {'name': 'John Doe', '200': 2, '500': 1, '1': 0, 'count': 3},
                                     {'name': 'Jane Smith', '200': 5, '500': 2, '1': 1, 'count': 8}
                                 ]
                             }
                         ]
                     }
    """
    try:
        recipient_email = data.get('recipient_email')
        report_date = data.get('date', timezone.now().strftime("%B %Y"))

        if not recipient_email:
            print("Error: Recipient email not found in data.")
            return

        subject = f"Leasing Referrals Report - {report_date}"

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/leasing_referrals_report.html',
            {
                'data': data
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
        print(f"Leasing Referrals Report sent to {recipient_email}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending Leasing Referrals Report to {data.get('recipient_email', 'N/A')}: {e}")
