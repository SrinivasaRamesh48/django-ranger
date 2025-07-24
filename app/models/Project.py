from django.db import models

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    activation_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    domain_name = models.CharField(max_length=255, blank=True, null=True)
    free_month = models.BooleanField(default=False)
    qbo_customer_id = models.CharField(max_length=255, blank=True, null=True)
    rm_property_id = models.IntegerField(null=True, blank=True)

    # Relationships
    state = models.ForeignKey("UsState", on_delete=models.PROTECT, db_column='state_id')
    builder = models.ForeignKey("Builder", on_delete=models.SET_NULL, null=True, blank=True, db_column='builder_id')
    subscription_type = models.ForeignKey("SubscriptionType", on_delete=models.PROTECT, db_column='subscription_type_id')
    service_plan = models.ForeignKey("ServicePlan", on_delete=models.SET_NULL, null=True, blank=True, db_column='bulk_service_plan_id')
    circuit = models.ForeignKey("Circuit", on_delete=models.SET_NULL, null=True, blank=True, db_column='circuit_id')
    network_type = models.ForeignKey("ProjectNetworkType", on_delete=models.SET_NULL, null=True, blank=True, db_column='network_type_id')

    class Meta:
        db_table = "projects"
    def __str__(self):
        return self.name
    