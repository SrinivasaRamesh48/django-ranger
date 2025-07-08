from django.db import models
from .time_stamped_model_mixin import TimeStampedModelMixin  

class SubscriberPaymentMethod(TimeStampedModelMixin, models.Model):
    subscriber_payment_method_id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    card_exp_datetime = models.DateTimeField()
    merchant_payment_method_id = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(blank=True, null=True)
    subscriber = models.ForeignKey('Subscriber', on_delete=models.CASCADE, related_name='payment_methods', db_column='subscriber_id')
    

    class Meta:
        db_table = 'subscriber_payment_methods'