from django.db import models
class Payment(models.Model):
    """Django equivalent of the Laravel Payment model."""
    payment_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    merchant_id = models.CharField(max_length=255, blank=True, null=True)
    autopay_merchant_id = models.CharField(max_length=255, blank=True, null=True)
    qbo_payment_id = models.IntegerField(blank=True, null=True)

    # Relationships
    subscriber = models.ForeignKey('Subscriber', on_delete=models.CASCADE, db_column='subscriber_id')
    statement = models.ForeignKey('Statement', on_delete=models.CASCADE, db_column='statement_id')
    payment_method = models.ForeignKey('SubscriberPaymentMethod', on_delete=models.CASCADE, db_column='subscriber_payment_method_id')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']