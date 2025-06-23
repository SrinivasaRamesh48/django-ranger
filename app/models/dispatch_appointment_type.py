from django.db import models

class DispatchAppointmentType(models.Model):
    dispatch_appointment_type_id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'dispatch_appointment_types'
        app_label = 'app'

