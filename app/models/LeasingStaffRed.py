from django.db import models

class LeasingStaffRed(models.Model):
    leasing_staff_red_id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'leasing_staff_red' 
        app_label = 'app'

