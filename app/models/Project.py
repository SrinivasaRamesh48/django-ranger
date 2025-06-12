from django.db import models

# Import all related models
from .UsState import UsState
from .Builder import Builder
# Assuming SubscriptionType, ServicePlan, Circuit, ProjectNetworkType are defined
from .SubscriptionType import SubscriptionType # Import the related model
from .ServicePlan import ServicePlan # Import the related model
from .Circuit import Circuit # Import the related model
from .ProjectNetworkType import ProjectNetworkType # Import the related model

# For hasMany relationships, these will be implicitly available as reverse FKs
# from .Home import Home
# from .Node import Node
# from .NodeFrame import NodeFrame
# from .Uploads import Uploads
# from .ProjectAlert import ProjectAlert

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    circuit = models.ForeignKey(
        Circuit,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='circuit_id',
        related_name='projects_linked' 
    )
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True) # Assuming longer address string
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.ForeignKey(
        UsState,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='state_id',
        related_name='projects'
    )
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True) # Example precision for coords
    latitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True) # Example precision for coords
    builder = models.ForeignKey(
        Builder,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='builder_id',
        related_name='projects'
    )
    subscription_type = models.ForeignKey(
        SubscriptionType,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='subscription_type_id',
        related_name='projects'
    )
    service_plan = models.ForeignKey(
        ServicePlan,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='bulk_service_plan_id', # Matches Laravel's fillable field
        related_name='bulk_projects'
    )
    activation_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    domain_name = models.CharField(max_length=255, blank=True, null=True)
    free_month = models.BooleanField(default=False) # Assuming it's a flag
    qbo_customer_id = models.CharField(max_length=255, blank=True, null=True) # QuickBooks Online Customer ID
    rm_property_id = models.CharField(max_length=255, blank=True, null=True) # Some kind of property ID
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'projects'
        app_label = 'app'

    def __str__(self):
        return self.name
    