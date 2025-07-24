from django.db import models
from .time_stamped_model_mixin import TimeStampedModelMixin

class Subscriber(TimeStampedModelMixin, models.Model):
    subscriber_id = models.AutoField(primary_key=True)

    home = models.ForeignKey('Home', on_delete=models.SET_NULL, null=True, db_column='home_id', related_name='subscribers')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    primary_email = models.EmailField()
    username = models.CharField(max_length=150,)
    password = models.CharField(max_length=255)  # You will hash this in the view using make_password()

    primary_phone = models.CharField(max_length=20,null=True)
    service_plan = models.ForeignKey('ServicePlan', on_delete=models.SET_NULL, null=True, db_column='service_plan_id')
    node = models.ForeignKey('Node', on_delete=models.SET_NULL, null=True, db_column='node_id')

    node_port_number = models.CharField(max_length=50, null=True, blank=True)

    service_activated_on = models.DateTimeField(null=True, blank=True)
    service_deactivated_on = models.DateTimeField(null=True, blank=True)
    suspended = models.BooleanField(default=False)

    merchant_customer_id = models.CharField(max_length=100, null=True, blank=True)
    autopay_merchant_id = models.CharField(max_length=100, null=True, blank=True)
    acp_application_id = models.CharField(max_length=100, null=True, blank=True)
    qbo_customer_id = models.CharField(max_length=100, null=True, blank=True)
    multi_home_subscriber = models.BooleanField(default=False)
    pause_billing = models.BooleanField(default=False)

    class Meta:
        db_table = 'subscribers'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.subscriber_id})"