from django.db import models
from .subscriber import Subscriber # Import the Subscriber model
from .time_stamped_model_mixin import TimeStampedModelMixin  # Import the mixin for timestamp fields

class SubscriberPaymentMethod(TimeStampedModelMixin, models.Model):
    """Django equivalent of the Laravel SubscriberPaymentMethod model."""
    subscriber_payment_method_id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    card_exp_datetime = models.DateTimeField()
    merchant_payment_method_id = models.CharField(max_length=255)

    subscriber = models.ForeignKey('Subscriber', on_delete=models.CASCADE, related_name='payment_methods', db_column='subscriber_id')
    

    class Meta:
        db_table = 'subscriber_payment_methods'