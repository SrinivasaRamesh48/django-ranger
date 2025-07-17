from decimal import Decimal
from django.db import transaction
from django.conf import settings
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.models import Payment, Subscriber, Statement, StatementItem, StatementItemDescription, SubscriberPaymentMethod
from app.mail.payment_processed import send_payment_processed_email

@method_decorator(transaction.atomic, name='dispatch')
class CreateTransactionWebhookView(APIView):
    
    # Handles the POST request from the payment provider.
    def post(self, request, *args, **kwargs):
        try:
            payload_data = request.data.get('data', {}).get('object', {})

            if not payload_data.get('id'):
                return Response({'error': 'Invalid payload structure'}, status=status.HTTP_400_BAD_REQUEST)

            if Payment.objects.filter(merchant_id=payload_data['id']).exists():
                return Response({'status': 'success', 'message': 'Already processed'}, status=status.HTTP_200_OK)

            # --- Subscriber Identification ---
            subscriber_id_from_meta = payload_data.get('metadata', {}).get('subscriber_id')
            autopay_id = None

            if subscriber_id_from_meta:
                subscriber = Subscriber.objects.get(pk=subscriber_id_from_meta)
            else:
                customer_id = payload_data.get('customer')
                if not customer_id:
                     return Response({'error': 'Customer ID missing from payload'}, status=status.HTTP_400_BAD_REQUEST)
                subscriber = Subscriber.objects.get(merchant_customer_id=customer_id)
                autopay_id = subscriber.autopay_merchant_id

            # --- Find Related Objects ---
            statement = Statement.objects.filter(subscriber=subscriber, archived=False).first()
            if not statement:
                return Response({'error': f'No active statement found for subscriber {subscriber.id}'}, status=status.HTTP_404_NOT_FOUND)

            payment_method = SubscriberPaymentMethod.objects.get(merchant_payment_method_id=payload_data['payment_method'])
            
            # --- Create Database Records ---
            amount_received = Decimal(payload_data['amount_received']) / Decimal('100.0')
            payment = Payment.objects.create(
                subscriber=subscriber,
                statement=statement,
                amount=amount_received,
                subscriber_payment_method=payment_method,
                autopay_merchant_id=autopay_id,
                merchant_id=payload_data['id']
            )

            item_desc, _ = StatementItemDescription.objects.get_or_create(
                description="Payment Received. Thank you."
            )

            StatementItem.objects.create(
                statement=statement,
                description=item_desc,
                amount=amount_received * -1,
                payment=payment
            )

            # --- Update Statement Balance ---
            if statement.amount_past_due > 0:
                new_past_due = statement.amount_past_due - amount_received
                statement.amount_past_due = max(Decimal('0.00'), new_past_due)
                statement.save(update_fields=['amount_past_due'])

            # --- Send Email Notification (Using the Celery task) ---
            if not settings.DEBUG and subscriber.primary_email:
                email_data = {
                    'subscriber': {
                        'first_name': subscriber.first_name,
                        'email': subscriber.primary_email,
                    },
                    'payment_amount': f"{payment.amount:.2f}",
                }
                send_payment_processed_email.delay(email_data)

            return Response({'status': 'success', 'payment_id': payment.id}, status=status.HTTP_201_CREATED)

        except Subscriber.DoesNotExist:
            return Response({'error': 'Subscriber not found'}, status=status.HTTP_404_NOT_FOUND)
        except SubscriberPaymentMethod.DoesNotExist:
            return Response({'error': 'Payment method not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # In a real application, you should log this exception.
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)