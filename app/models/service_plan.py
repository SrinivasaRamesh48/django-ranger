from django.db import models
from app.models.time_stamped_model_mixin import TimeStampedModelMixin   

class ServicePlan(TimeStampedModelMixin, models.Model):
    service_plan_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'service_plans'
        

    def __str__(self):
        return self.name or f"Service Plan {self.service_plan_id}"