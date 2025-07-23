from django.db import models
from .user import User
from .service_change_schedule import ServiceChangeSchedule
from .time_stamped_model_mixin import TimeStampedModelMixin


class TicketEntry(TimeStampedModelMixin, models.Model):
    ticket_entry_id = models.AutoField(primary_key=True)
    description = models.TextField()
    notes_private = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    submitted = models.IntegerField(default=0)
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, related_name='entries', db_column='ticket_id')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='user_id')
    dispatch_appointment = models.OneToOneField('DispatchAppointment',on_delete=models.SET_NULL,null=True,blank=True,db_column='dispatch_appointment_id',related_name='ticket_entry',)
    class Meta:
        db_table = 'ticket_entry'
        ordering = ['-created_at']

    @property
    def service_change_schedule(self):
        try:
            return self.servicechangeschedule
        except ServiceChangeSchedule.DoesNotExist:
            return None