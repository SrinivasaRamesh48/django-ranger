from django.db import transaction
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
import decimal

# --- Assumed imports for custom classes ---
# In a real project, these classes would be defined in separate files.
# from .emails import PaymentProcessed, BillingPaymentProcessed
# from .qbo_controller import QBOController

from app.models import (
    Subscriber, Statement, Payment, SubscriberPaymentMethod,
    StatementItem, StatementItemDescription
)

class SuccessfulTransactionWebhookView(APIView):
    """
    Handles the 'successful_transaction_webhook' from a payment provider (e.g., Stripe).
    Corresponds to BillingController@create_transaction.
    
    NOTE: In a production environment, you MUST secure this webhook.
    This can be done by verifying a signature sent in the request headers.
    """
    permission_classes = [AllowAny] # Webhooks come from an external service, not a user.

    @transaction.atomic # Ensures all database operations in this block are one single transaction.
    def post(self, request, *args, **kwargs):
        payload = request.data
        
        # 1. Validate payload structure and get the core data object
        try:
            data = payload['data']['object']
            merchant_id = data['id']
        except KeyError:
            return Response({'error': 'Invalid payload structure'}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Check if this payment has already been processed
        # Laravel: $existing_payment = Payment::where('merchant_id', $data['id'])->first();
        if Payment.objects.filter(merchant_id=merchant_id).exists():
            return Response({'status': 'Already processed'}, status=status.HTTP_200_OK)

        # 3. Determine the subscriber and autopay ID
        try:
            if 'subscriber_id' in data.get('metadata', {}):
                subscriber = Subscriber.objects.get(subscriber_id=data['metadata']['subscriber_id'])
                autopay_id = None
            else:
                subscriber = Subscriber.objects.get(merchant_customer_id=data['customer'])
                autopay_id = subscriber.autopay_merchant_id

            # 4. Get related objects needed for creation
            statement = Statement.objects.get(subscriber=subscriber, archived=False)
            payment_method = SubscriberPaymentMethod.objects.get(merchant_payment_method_id=data['payment_method'])
            item_description = StatementItemDescription.objects.get(description="Payment Received. Thank you.")
            
        except Subscriber.DoesNotExist:
            return Response({'error': 'Subscriber not found'}, status=status.HTTP_404_NOT_FOUND)
        except (Statement.DoesNotExist, SubscriberPaymentMethod.DoesNotExist, StatementItemDescription.DoesNotExist) as e:
            return Response({'error': f'Configuration error: {str(e)}'}, status=status.HTTP_404_NOT_FOUND)

        # 5. Create the Payment and StatementItem records
        amount_received = decimal.Decimal(data['amount_received']) / 100

        payment = Payment.objects.create(
            subscriber=subscriber,
            statement=statement,
            amount=amount_received,
            subscriber_payment_method=payment_method,
            autopay_merchant_id=autopay_id,
            merchant_id=merchant_id
        )

        StatementItem.objects.create(
            statement=statement,
            statement_item_description=item_description,
            amount=amount_received * -1,
            payment=payment
        )

        # 6. Update the statement's past due amount
        if statement.amount_past_due > 0:
            new_past_due = statement.amount_past_due - amount_received
            statement.amount_past_due = max(new_past_due, decimal.Decimal('0.00'))
            statement.save()

        # 7. Send confirmation email in production
        if not settings.DEBUG:
            if subscriber.primary_email:
                # This logic assumes you have a PaymentProcessed class that handles
                # building and sending the email, similar to a Laravel Mailable.
                email_context = {
                    'subscriber': subscriber,
                    'payment_amount': amount_received
                }
                # Example of how you would call your custom class:
                # email = PaymentProcessed(context=email_context)
                # email.send(to_email=subscriber.primary_email)
                # Since the implementation is in another file, we'll keep the direct
                # send_mail call here as a functional placeholder.
                payment_amount_str = f"{amount_received:.2f}"
                send_mail(
                    subject='Your Payment Has Been Processed',
                    message=f'Hi {subscriber.first_name},\n\nThank you for your payment of ${payment_amount_str}.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.primary_email],
                    fail_silently=False,
                )

        # 8. All commented-out logic from Laravel is translated below as comments.
        
        # --- Internal Billing Notification Email ---
        # payment_email_data = {
        #     'subscriber_name': f"{subscriber.first_name} {subscriber.last_name}",
        #     'amount': f"{amount_received:.2f}",
        #     'method': payment_method.nickname,
        #     'timestamp': timezone.datetime.fromtimestamp(data['created'], tz=timezone.utc),
        #     'merchant_id': merchant_id
        # }
        # The line below would use your custom BillingPaymentProcessed mailable class
        # BillingPaymentProcessed(context=payment_email_data).send(to_email="jchapman@uprisefiber.com")

        # --- QBO Integration ---
        # if subscriber.qbo_customer_id:
        #     qbo_controller = QBOController()
        #     payment_data = {
        #         "CustomerRef": {"value": subscriber.qbo_customer_id},
        #         'PaymentMethodRef': {'value': settings.QBO_STRIPE_PAYMENT_METHOD_ID},
        #         "DepositToAccountRef": {'value': settings.QBO_DEPOSIT_TO_ID},
        #         "TotalAmt": amount_received,
        #         "Line": [{
        #             "Amount": amount_received,
        #             "LinkedTxn": [{
        #                 "TxnId": statement.qbo_invoice_id,
        #                 "TxnType": "Invoice"
        #             }]
        #         }]
        #     }
        #     data_service = qbo_controller.connect()
        #     payment_obj = qbo_controller.create_payment(data_service, payment_data)
        #     payment.qbo_payment_id = payment_obj.Id
        #     payment.save(update_fields=['qbo_payment_id'])
        
        return Response({'status': 'Transaction created successfully'}, status=status.HTTP_201_CREATED)