from django.db import models
from .service_change_schedule_type import ServiceChangeScheduleType 
from .subscriber import Subscriber 
from .service_plan import ServicePlan 
from .ticket import Ticket
from .leasing_staff_red import LeasingStaffRed 
from .time_stamped_model_mixin import TimeStampedModelMixin

class ServiceChangeSchedule(TimeStampedModelMixin, models.Model):
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
    ticket_entry = models.ForeignKey('TicketEntry', on_delete=models.CASCADE, db_column='ticket_entry_id', related_name='service_change_schedule')
    leasing_staff_red = models.ForeignKey(LeasingStaffRed, on_delete=models.SET_NULL, null=True, blank=True, db_column='leasing_staff_red_id')

    
    class Meta:
        db_table = 'service_change_schedule'