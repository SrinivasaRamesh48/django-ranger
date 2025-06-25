from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# ... (previous tasks in the same file)

@shared_task
def send_vineyards_monday_message_email(data):
    """
    A Celery task to send the Vineyards Monday message about upcoming
    wifi credential updates.

    Args:
        data (dict): A dictionary containing the message details.
                     Example:
                     {
                         'recipient_email': 'subscriber@example.com',
                         'subscriber_name': 'Jane Doe',
                         'ssid1': 'Vineyards-UnitA1-2.4G',
                         'ssid2': 'Vineyards-UnitA1-5G',
                         'passkey': 'newpassword123'
                     }
    """
    try:
        recipient_email = data.get('recipient_email')
        if not recipient_email:
            print("Error: Recipient email not found in data.")
            return

        subject = "Uprise Fiber - Wifi Credentials Updating Tomorrow"
        from_email = settings.DEFAULT_FROM_EMAIL

        # Render the HTML content for the email from a Django template.
        html_message = render_to_string(
            'mail/vineyards_monday_message.html',
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
        print(f"Vineyards Monday message sent to {recipient_email}")

    except Exception as e:
        # Log any exceptions that occur during email sending.
        print(f"Error sending Vineyards Monday message: {e}")
