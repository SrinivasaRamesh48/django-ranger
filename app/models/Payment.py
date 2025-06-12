from django.db import models
# Import related models
from .Subscriber import Subscriber 
from .Statement import Statement 
from .SubscriberPaymentMethod import SubscriberPaymentMethod # Assuming SubscriberPaymentMethod model exists

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    subscriber = models.ForeignKey(
        Subscriber,
        on_delete=models.CASCADE, 
        db_column='subscriber_id',
        related_name='payments'
    )
    statement = models.ForeignKey(
        Statement,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='statement_id',
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2) # Use DecimalField for currency
    merchant_id = models.CharField(max_length=255) # Assuming this is an external ID string
    payment_method = models.ForeignKey(
        SubscriberPaymentMethod,
        on_delete=models.SET_NULL, # Assuming payment might remain if payment method is deleted
        null=True, blank=True,
        db_column='subscriber_payment_method_id',
        related_name='payments'
    )
    autopay_merchant_id = models.CharField(max_length=255, null=True, blank=True) # Assuming string, nullable
    qbo_payment_id = models.CharField(max_length=255, null=True, blank=True) # Assuming string, nullable, for QuickBooks Online
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        app_label = 'app'

    def __str__(self):
        return f"Payment {self.payment_id} - Amount: {self.amount}"