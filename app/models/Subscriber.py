from django.db import models
from django.contrib.auth.hashers import make_password, check_password # For password hashing

# Import all related models
from .Home import Home
from .ServicePlan import ServicePlan
from .Node import Node # Assuming Node model exists
# For hasMany relationships, these will be implicitly available as reverse FKs:
# from .Ticket import Ticket
# from .Uploads import Uploads
# from .Statement import Statement
# from .Payment import Payment
# from .SubscriberPaymentMethod import SubscriberPaymentMethod
# from .MultiHomeSubscriberHome import MultiHomeSubscriberHome
# from .SubscriberAlert import SubscriberAlert

class Subscriber(models.Model):
    subscriber_id = models.AutoField(primary_key=True)
    home = models.ForeignKey(
        Home,
        on_delete=models.CASCADE, # Assuming deleting a home cascades to its subscribers
        db_column='home_id',
        related_name='subscribers_at_home' # Renamed to avoid clash with 'subscribers' reverse relation
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    primary_email = models.EmailField(unique=True) # Assuming email is unique
    username = models.CharField(max_length=255, unique=True) # Assuming username is unique
    # Password field - will store hashed passwords
    password = models.CharField(max_length=255) # Max_length for hashed password
    primary_phone = models.CharField(max_length=20, blank=True, null=True) # E.g., for E.164 format

    service_plan = models.ForeignKey(
        ServicePlan,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='service_plan_id',
        related_name='subscribers'
    )
    node = models.ForeignKey(
        Node,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='node_id',
        related_name='subscribers'
    )
    node_port_number = models.IntegerField(blank=True, null=True)

    service_activated_on = models.DateTimeField(null=True, blank=True)
    service_deactivated_on = models.DateTimeField(null=True, blank=True)
    suspended = models.BooleanField(default=False)

    merchant_customer_id = models.CharField(max_length=255, blank=True, null=True)
    autopay_merchant_id = models.CharField(max_length=255, blank=True, null=True)
    acp_application_id = models.CharField(max_length=255, blank=True, null=True) # Affordable Connectivity Program ID
    qbo_customer_id = models.CharField(max_length=255, blank=True, null=True) # QuickBooks Online Customer ID

    multi_home_subscriber = models.BooleanField(default=False) # Flag indicating multi-home status
    pause_billing = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subscribers'
        app_label = 'app'

    def __str__(self):
        return f"Subscriber {self.subscriber_id} - {self.username}"

    # --- Custom methods for Laravel's dynamic relations/logic ---

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def open_tickets_info(self):
        # Equivalent of Laravel's `where("ticket_status_id", "<>", 1)`
        # Assuming Ticket model has 'ticket_status' FK to TicketStatus, and status_id=1 means 'closed'
        try:
            from .Ticket import Ticket # Import locally
            return self.tickets.exclude(ticket_status__status_id=1).all() # Or exclude(ticket_status_id=1) if direct FK
        except AttributeError:
            return Ticket.objects.none() # Return empty queryset if Ticket model not ready

    @property
    def current_statement(self):
        # Equivalent of Laravel's `where("archived", 0)`
        # Assuming Statement model has 'archived' BooleanField
        try:
            from .Statement import Statement # Import locally
            return self.statements.filter(archived=False).first()
        except AttributeError:
            return None

    @property
    def active_alerts(self):
        # Equivalent of Laravel's `where("active", 1)->orderByDesc('alert_type_id')`
        # Assuming SubscriberAlert model exists with 'active' and 'alert_type_id'
        try:
            from .SubscriberAlert import SubscriberAlert # Import locally
            return self.subscriber_alerts.filter(active=True).order_by('-alert_type_id') # Use default reverse relation name
        except AttributeError:
            return SubscriberAlert.objects.none()