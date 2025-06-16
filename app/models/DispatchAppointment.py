from django.db import models
from .DispatchAppointmentType import DispatchAppointmentType 
from .DispatchAppointmentTimeslot import DispatchAppointmentTimeslot 
from .Ticket import Ticket 
from .User import User 

class DispatchAppointment(models.Model):
    """Django equivalent of the Laravel DispatchAppointment model."""
    dispatch_appointment_id = models.AutoField(primary_key=True)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    completion_notes = models.TextField(blank=True, null=True)
    completed_on = models.DateTimeField(blank=True, null=True)
    canceled_on = models.DateTimeField(blank=True, null=True)
    wiring_certified = models.BooleanField(default=False)
    wiring_repaired = models.BooleanField(default=False)
    pte = models.BooleanField(default=False) # Permission To Enter
    pets = models.BooleanField(default=False) # Are there pets on premise?

    # Relationships
    appointment_type = models.ForeignKey(DispatchAppointmentType, on_delete=models.CASCADE, db_column='dispatch_appointment_type_id')
    technician = models.ForeignKey(User, related_name='dispatches', on_delete=models.CASCADE, db_column='user_id')
    timeslot = models.ForeignKey(DispatchAppointmentTimeslot, on_delete=models.CASCADE, db_column='dispatch_appointment_timeslot_id')
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, blank=True, null=True, db_column='ticket_id')
    created_by = models.ForeignKey(User, related_name='created_appointments', on_delete=models.CASCADE, db_column='created_by_id')
    canceled_by = models.ForeignKey(User, related_name='canceled_appointments', on_delete=models.SET_NULL, blank=True, null=True, db_column='canceled_by')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "dispatch_appointments"
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.appointment_type.name} for Ticket {self.ticket_id} on {self.date}"