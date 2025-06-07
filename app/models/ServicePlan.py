from django.db import models

class ServicePlan(models.Model):
    service_plan_id = models.AutoField(primary_key=True)
    # Assuming common fields for a service plan. Adjust these based on your actual database schema.
    name = models.CharField(max_length=255, unique=True) # E.g., "Basic Plan", "Premium Plan"
    description = models.TextField(blank=True, null=True)
    speed_mbps = models.IntegerField(blank=True, null=True) # E.g., 100 for 100 Mbps
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # Price of the plan
    active = models.BooleanField(default=True) # Whether the plan is currently active/offered
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'service_plans'
        app_label = 'app'

    def __str__(self):
        return self.name or f"Service Plan {self.service_plan_id}"