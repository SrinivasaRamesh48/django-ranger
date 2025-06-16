from django.db import models

# Import all related models
from .ServiceChangeScheduleType import ServiceChangeScheduleType # Ensure this model exists
from .Subscriber import Subscriber # Ensure this model exists
from .ServicePlan import ServicePlan # Ensure this model exists
from .Ticket import Ticket # Ensure this model exists (note: Laravel uses ticket_entry_id, assuming Ticket model)
from .LeasingStaffRed import LeasingStaffRed # Ensure this model exists

class ServiceChangeSchedule(models.Model):
    """Django equivalent of the Laravel ServiceChangeSchedule model."""
    service_change_schedule_id = models.AutoField(primary_key=True)
    ssid_1 = models.CharField(max_length=255, blank=True, null=True)
    passkey_1 = models.CharField(max_length=255, blank=True, null=True)
    ssid_2 = models.CharField(max_length=255, blank=True, null=True)
    passkey_2 = models.CharField(max_length=255, blank=True, null=True)
    process_on = models.DateField()
    processed = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)

    # Relationships
    service_change_schedule_type = models.ForeignKey(ServiceChangeScheduleType, on_delete=models.PROTECT, db_column='service_change_schedule_type_id')
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, db_column='subscriber_id')
    service_plan = models.ForeignKey(ServicePlan, on_delete=models.PROTECT, db_column='service_plan_id')
    ticket_entry = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True, blank=True, db_column='ticket_entry_id')
    leasing_staff_red = models.ForeignKey(LeasingStaffRed, on_delete=models.SET_NULL, null=True, blank=True, db_column='leasing_staff_red_id')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'service_change_schedule'