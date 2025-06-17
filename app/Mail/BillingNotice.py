from ranger.celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_billing_notice_email(data):
    """
    A Celery task to send a billing notice email using the HTML body
    provided directly from the frontend.

    Args:
        data (dict): A dictionary containing the email details. It must
                     include 'email' (the recipient) and 'body' (the full HTML).
    """
    recipient_email = data.get('email')
    if not recipient_email:
        print("Error: No recipient email provided for billing notice.")
        return

    subject = "Uprise Fiber - Billing Notice"
    html_body = data.get('body', '')

    try:
        send_mail(
            subject=subject,
            message="",  # Plain text is optional when HTML is provided
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_body,
        )
        print(f"Billing notice queued for {recipient_email}")
    except Exception as e:
        print(f"Failed to send billing notice to {recipient_email}: {e}")
        
        
""""  How to Use It
# from .tasks import send_billing_notice_email

def some_view_that_triggers_the_notice(request):
    # The data comes from your frontend's request
    email_details = {
        "email": "customer@example.com",
        "body": "<html><body>...your complete HTML from React...</body></html>"
    }
    
    # Send the task to Celery to run in the background
    send_billing_notice_email.delay(email_details)
    
    return Response({"status": "Billing notice is being sent."})   """        