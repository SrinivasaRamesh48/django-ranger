from django.db import models
from .time_stamped_model_mixin import TimeStampedModelMixin

class LeasingStaffRed(TimeStampedModelMixin, models.Model):
    leasing_staff_red_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'leasing_staff_red' 
        app_label = 'app'

