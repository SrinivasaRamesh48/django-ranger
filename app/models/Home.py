from django.db import models
from app.models.Project import Project
from app.models.UsState import UsState
from app.models.MacAddress import MacAddress
from app.models.Node import Node
from django.conf import settings

class Home(models.Model):
    """
    Django model equivalent of the Laravel 'Home' Eloquent model.
    """
    home_id = models.AutoField(primary_key=True)

    # Foreign Key fields (equivalent to hasOne where FK is on the 'homes' table)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    us_state = models.ForeignKey(UsState, on_delete=models.SET_NULL, null=True, blank=True, db_column='state_id')
    mac_address = models.ForeignKey(MacAddress, on_delete=models.SET_NULL, null=True, blank=True ,related_name="mac_address_ID")
    node = models.ForeignKey(Node, on_delete=models.SET_NULL, null=True, blank=True)
    wiring_certified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='certified_homes'
    )

    # Standard fields
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    unit = models.CharField(max_length=50, null=True, blank=True)
    subscriber_name = models.CharField(max_length=255, null=True, blank=True) # Renamed from 'subsciber'
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    node_switch_unit = models.IntegerField(null=True, blank=True)
    node_switch_module = models.IntegerField(null=True, blank=True)
    node_port_num = models.IntegerField(null=True, blank=True)
    wiring_certified_on = models.DateField(null=True, blank=True)
    exclude_from_reports = models.BooleanField(default=False)

    # Automatic timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'homes'
        app_label = 'app'
        
        
    def __str__(self):
        return f"{self.address}, {self.city}"

    # --- Properties for Business Logic ---
    # These replace the relationships with 'where' clauses from Laravel.

    @property
    def active_subscriber(self):
        """
        Returns the active subscriber for this home based on specific business rules.
        This replaces the 'active_subscriber' relationship in Laravel.
        """
        return self.subscribers.filter(
            service_activated_on__isnull=False,
            service_deactivated_on__isnull=True
        ).exclude(service_plan_id=1).first()