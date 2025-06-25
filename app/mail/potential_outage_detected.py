from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# ... (previous tasks in the same file)

@shared_task
def send_potential_outage_detected_email(data):
    """
    A Celery task to send a potential outage detection alert.

    Args:
        data (dict): A dictionary containing the alert details.
                     Example:
                     {
                         'recipient_email': 'network-ops@example.com',
                         'project': 'Verso Apartments',
                         'url': 'https://ranger.uprisefiber.com/outages/confirm/some_token'
                     }
    """
    try:
        recipient_email = data.get('recipient_email')
        project_name = data.get('project')
        
        if not all([recipient_email, project_name]):
            print("Error: recipient_email and project name are required.")
            return

        # The subject of the email, dynamically including the project name.
        subject = f"Potential Outage Detected - {project_name}"

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/potential_outage_detected.html',
            {'data': data}
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
        print(f"Potential outage notification sent to {recipient_email} for project {project_name}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending potential outage notification: {e}")
