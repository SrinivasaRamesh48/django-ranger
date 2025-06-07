from django.db import models

# Import all related models
from .ServiceChangeScheduleType import ServiceChangeScheduleType # Ensure this model exists
from .Subscriber import Subscriber # Ensure this model exists
from .ServicePlan import ServicePlan # Ensure this model exists
from .Ticket import Ticket # Ensure this model exists (note: Laravel uses ticket_entry_id, assuming Ticket model)
from .LeasingStaffRed import LeasingStaffRed # Ensure this model exists

class ServiceChangeSchedule(models.Model):
    service_change_schedule_id = models.AutoField(primary_key=True)
    service_change_schedule_type = models.ForeignKey(
        ServiceChangeScheduleType,
        on_delete=models.CASCADE, # If the type is deleted, these schedules go too
        db_column='service_change_schedule_type_id',
        related_name='service_change_schedules'
    )
    subscriber = models.ForeignKey(
        Subscriber,
        on_delete=models.CASCADE, # If subscriber is deleted, schedule is removed
        db_column='subscriber_id',
        related_name='service_change_schedules'
    )
    service_plan = models.ForeignKey(
        ServicePlan,
        on_delete=models.SET_NULL, # Assuming schedule might remain if service plan is deleted
        null=True, blank=True,
        db_column='service_plan_id',
        related_name='service_change_schedules'
    )
    # Laravel's 'ticket_entry_id' typically refers to a Ticket ID.
    ticket_entry = models.ForeignKey(
        Ticket,
        on_delete=models.SET_NULL, # Assuming schedule might remain if ticket is deleted
        null=True, blank=True,
        db_column='ticket_entry_id',
        related_name='service_change_schedules'
    )
    ssid_1 = models.CharField(max_length=255, blank=True, null=True) # SSID for network 1
    passkey_1 = models.CharField(max_length=255, blank=True, null=True) # Passkey for network 1 (potentially encrypted)
    ssid_2 = models.CharField(max_length=255, blank=True, null=True) # SSID for network 2
    passkey_2 = models.CharField(max_length=255, blank=True, null=True) # Passkey for network 2 (potentially encrypted)
    leasing_staff_red = models.ForeignKey(
        LeasingStaffRed,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='leasing_staff_red_id',
        related_name='service_change_schedules'
    )
    process_on = models.DateField(null=True, blank=True) # The date when the change should be processed
    processed = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'service_change_schedule' # Note: Table name is singular as per Laravel model
        app_label = 'app'

    def __str__(self):
        return f"Service Change Schedule {self.service_change_schedule_id} - Subscriber: {self.subscriber_id}"