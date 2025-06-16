from django.db import models
from .Subscriber import Subscriber # Import the Subscriber model

class SubscriberPaymentMethod(models.Model):
    """Django equivalent of the Laravel SubscriberPaymentMethod model."""
    subscriber_payment_method_id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    card_exp_datetime = models.DateTimeField()
    merchant_payment_method_id = models.CharField(max_length=255)

    # Relationship
    subscriber = models.ForeignKey('Subscriber', on_delete=models.CASCADE, related_name='payment_methods', db_column='subscriber_id')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'subscriber_payment_methods'