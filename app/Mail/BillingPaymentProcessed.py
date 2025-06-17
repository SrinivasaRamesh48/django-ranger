
from ranger.celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_billing_payment_processed_email(data):
    """
    Sends a "payment processed" email using the HTML body
    provided directly from the front-end via the API.
    """
    recipient_email = data.get('email')
    if not recipient_email:
        return

    subject = "Ranger - Payment Processed"
    
    # The 'body' is the complete HTML string sent from your React app
    html_body = data.get('body', '')

    send_mail(
        subject=subject,
        message="", # Plain text is optional
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        html_message=html_body,
    )