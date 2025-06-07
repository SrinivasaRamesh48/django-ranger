from django.db import models
from .DispatchAppointmentType import DispatchAppointmentType 
from .DispatchAppointmentTimeslot import DispatchAppointmentTimeslot 
from .Ticket import Ticket 
from .User import User 

class DispatchAppointment(models.Model):
    dispatch_appointment_id = models.AutoField(primary_key=True)
    dispatch_appointment_type = models.ForeignKey(
        DispatchAppointmentType,
        on_delete=models.CASCADE,
        db_column='dispatch_appointment_type_id',
        related_name='dispatch_appointments'
    )
    technician = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='user_id', 
        related_name='assigned_dispatch_appointments'
    )
    date = models.DateField()
    timeslot = models.ForeignKey(
        DispatchAppointmentTimeslot,
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        db_column='dispatch_appointment_timeslot_id',
        related_name='dispatch_appointments'
    )
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE, 
        db_column='ticket_id',
        related_name='dispatch_appointments'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='created_by_id',
        related_name='created_dispatch_appointments'
    )
    notes = models.TextField(blank=True, null=True)
    completion_notes = models.TextField(blank=True, null=True)
    completed_on = models.DateTimeField(blank=True, null=True)
    wiring_certified = models.BooleanField(default=False) 
    wiring_repaired = models.BooleanField(default=False)  
    canceled_on = models.DateTimeField(blank=True, null=True)
    canceled_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='canceled_by', 
        related_name='canceled_dispatch_appointments'
    )
    pte = models.TextField(blank=True, null=True) 
    pets = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dispatch_appointments'
        app_label = 'app'

    def __str__(self):
        return f"Dispatch Appointment {self.dispatch_appointment_id} for Ticket {self.ticket_id}"