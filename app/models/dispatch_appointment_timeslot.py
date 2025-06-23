from django.db import models

class DispatchAppointmentTimeslot(models.Model):
    dispatch_appointment_timeslot_id = models.AutoField(primary_key=True)
    
    class Meta:
        db_table = 'dispatch_appointment_timeslots' 
        app_label = 'app'
