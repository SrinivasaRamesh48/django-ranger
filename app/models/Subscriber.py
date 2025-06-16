from django.db import models

class Subscriber(models.Model):
    subscriber_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    primary_email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    primary_phone = models.CharField(max_length=20, blank=True, null=True)
    service_activated_on = models.DateTimeField(null=True, blank=True)
    service_deactivated_on = models.DateTimeField(null=True, blank=True)
    suspended = models.BooleanField(default=False)
    merchant_customer_id = models.CharField(max_length=255, blank=True, null=True)
    autopay_merchant_id = models.CharField(max_length=255, blank=True, null=True)
    acp_application_id = models.CharField(max_length=255, blank=True, null=True)
    qbo_customer_id = models.CharField(max_length=255, blank=True, null=True)
    multi_home_subscriber = models.BooleanField(default=False)
    pause_billing = models.BooleanField(default=False)
    
    # Relationships
    home = models.ForeignKey("Home", on_delete=models.PROTECT, db_column='home_id')
    service_plan = models.ForeignKey("ServicePlan", on_delete=models.PROTECT, db_column='service_plan_id')
    node = models.ForeignKey("Node", on_delete=models.SET_NULL, null=True, blank=True, db_column='node_id')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'subscribers'
        
    @property
    def open_tickets(self):
        # Assuming ticket_status_id for 'closed' is 1
        return self.tickets.exclude(ticket_status_id=1)

    @property
    def active_statement(self):
        return self.statements.filter(archived=False).first()

    @property
    def active_alerts(self):
        return self.alerts.filter(active=True).order_by('-alert_type_id')