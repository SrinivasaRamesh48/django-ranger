from django.db import models
from .Subscriber import Subscriber # Import the Subscriber model

class SubscriberPaymentMethod(models.Model):
    subscriber_payment_method_id = models.AutoField(primary_key=True)
    subscriber = models.ForeignKey(
        Subscriber,
        on_delete=models.CASCADE, # If subscriber is deleted, payment methods are too
        db_column='subscriber_id',
        related_name='payment_methods' # Reverse relation from Subscriber to SubscriberPaymentMethod
    )
    nickname = models.CharField(max_length=255, blank=True, null=True) # E.g., "My Visa", "Work Card"
    # Assuming card_exp_datetime stores a full datetime, if just date, use models.DateField
    card_exp_datetime = models.DateTimeField(blank=True, null=True)
    merchant_payment_method_id = models.CharField(max_length=255) # External ID from payment merchant
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subscriber_payment_methods'
        app_label = 'app'

    def __str__(self):
        return f"Payment Method {self.subscriber_payment_method_id} for Subscriber {self.subscriber_id} - {self.nickname or 'N/A'}"