from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import decimal

# ... (previous tasks in the same file)

@shared_task
def send_projects_report_email(data):
    """
    A Celery task to compile and send the detailed Projects Report with an attachment.

    This task pre-calculates take rates before rendering the template.

    Args:
        data (dict): A dictionary containing the report data, recipient, and attachment path.
                     Example:
                     {
                         'recipient_email': 'report-recipient@example.com',
                         'attachment_path': '/path/to/report.csv',
                         'start_date': '2025-05-01',
                         'end_date': '2025-05-31',
                         'optin_summary': { ... },
                         'optin_projects': [ ... ],
                         'bulk_summary': { ... },
                         'bulk_projects': [ ... ]
                     }
    """
    try:
        recipient_email = data.get('recipient_email')
        attachment_path = data.get('attachment_path')

        if not all([recipient_email, attachment_path]):
            print("Error: recipient_email and attachment_path are required.")
            return

        # --- Pre-calculation logic for template ---
        # Calculate take rates to avoid complex logic in the template.
        def calculate_rates(summary, projects):
            if summary.get('total_units', 0) > 0:
                summary['take_rate'] = (decimal.Decimal(summary['active']) / decimal.Decimal(summary['total_units'])) * 100
            else:
                summary['take_rate'] = 0
            
            for project in projects:
                if project.get('total_units', 0) > 0:
                    project['take_rate'] = (decimal.Decimal(project['active']) / decimal.Decimal(project['total_units'])) * 100
                else:
                    project['take_rate'] = 0

        calculate_rates(data['optin_summary'], data['optin_projects'])
        calculate_rates(data['bulk_summary'], data['bulk_projects'])
        # --- End pre-calculation ---

        # Calculate the name of last month for the subject.
        today = timezone.now().date()
        first_day_of_current_month = today.replace(day=1)
        last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
        report_month_str = last_day_of_last_month.strftime("%B %Y")

        # The subject of the email.
        subject = f"Uprise Fiber Projects Report - {report_month_str}"

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # Render the HTML content for the email from a Django template.
        html_body = render_to_string(
            'mail/projects_report.html',
            {
                'data': data,
                'date': report_month_str
            }
        )

        # Create an EmailMessage instance to handle the attachment.
        email = EmailMessage(
            subject=subject,
            body=html_body,
            from_email=from_email,
            to=[recipient_email],
        )
        email.content_subtype = "html"  # Set content type to HTML
        email.attach_file(attachment_path) # Attach the file
        email.send(fail_silently=False) # Send the email

        print(f"Projects Report sent to {recipient_email}")

    except FileNotFoundError:
        print(f"Error sending Projects Report: Attachment not found at {data.get('attachment_path')}")
    except Exception as e:
        print(f"Error sending Projects Report to {data.get('recipient_email', 'N/A')}: {e}")

