from django.db import models
from django.contrib.auth.hashers import make_password, check_password # For password hashing

class Subscriber(models.Model):
    subscriber_id = models.AutoField(primary_key=True)
    home = models.OneToOneField(
        'Home',
        on_delete=models.SET_NULL, # Or models.CASCADE, depending on your desired behavior
        db_column='home_id',
        null=True,
        blank=True,
        related_name='subscriber_home' # Renamed for clarity to avoid clash
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    primary_email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255) 
    primary_phone = models.CharField(max_length=20, blank=True, null=True)
    service_plan = models.ForeignKey(
        'ServicePlan',
        on_delete=models.SET_NULL,
        db_column='service_plan_id',
        null=True,
        blank=True
    )
    node_id = models.IntegerField(blank=True, null=True)
    node_port_number = models.IntegerField(blank=True, null=True)
    service_activated_on = models.DateTimeField(blank=True, null=True)
    service_deactivated_on = models.DateTimeField(blank=True, null=True)
    suspended = models.BooleanField(default=False)
    merchant_customer_id = models.CharField(max_length=255, blank=True, null=True)
    autopay_merchant_id = models.CharField(max_length=255, blank=True, null=True)
    acp_application_id = models.CharField(max_length=255, blank=True, null=True)
    qbo_customer_id = models.CharField(max_length=255, blank=True, null=True)
    multi_home_subscriber = models.BooleanField(default=False)
    pause_billing = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "subscribers" # Specifies the database table name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # Relationships (similar to Laravel's relationships)
    # The related_name attribute allows you to access related objects from the reverse side of the relationship.

    def open_tickets(self):
        return self.tickets.exclude(ticket_status_id=1)

    def statement_active(self):
        return self.statements.filter(archived=False).first()

    def active_alerts(self):
        return self.alerts.filter(active=True).order_by('-alert_type_id')