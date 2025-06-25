from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

# ... (previous tasks in the same file)

@shared_task
def send_default_credentials_list_email(data):
    """
    A Celery task to send an email with an attachment, such as a credentials list.

    This task uses Django's EmailMessage class to handle attachments.

    Args:
        data (dict): A dictionary containing the necessary data for the email.
                     Example:
                     {
                         'recipient_email': 'user@example.com',
                         'subject': 'Your Default Credentials',
                         'attachment_path': '/path/to/your/file.pdf'
                     }
    """
    try:
        recipient_email = data.get('recipient_email')
        subject = data.get('subject')
        attachment_path = data.get('attachment_path')

        if not all([recipient_email, subject, attachment_path]):
            print("Error: recipient_email, subject, and attachment_path are required.")
            return

        # The sender's email address from settings.
        from_email = settings.DEFAULT_FROM_EMAIL

        # Render the simple HTML body from a template.
        html_body = render_to_string(
            'mail/default_credentials_list.html',
            {'data': data}
        )

        # Create an EmailMessage instance.
        email = EmailMessage(
            subject=subject,
            body=html_body,
            from_email=from_email,
            to=[recipient_email],
        )
        
        # Set the content type to HTML.
        email.content_subtype = "html"

        # Attach the file.
        email.attach_file(attachment_path)

        # Send the email.
        email.send(fail_silently=False)

        print(f"Default credentials email with attachment sent to {recipient_email}")

    except FileNotFoundError:
        print(f"Error sending credentials email: Attachment not found at {data.get('attachment_path')}")
    except Exception as e:
        # Log any other exceptions that occur.
        print(f"Error sending default credentials email to {data.get('recipient_email', 'N/A')}: {e}")
