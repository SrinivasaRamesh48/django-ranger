from django.db import models

class LeasingStaffRed(models.Model):
    leasing_staff_red_id = models.AutoField(primary_key=True)
    # Assuming this table holds some descriptive information, e.g., a name or identifier.
    # Add other fields here that correspond to columns in your 'leasing_staff_red' table.
    name = models.CharField(max_length=255, unique=True) # Example field

    class Meta:
        db_table = 'leasing_staff_red' # Note: Table name is singular as per Laravel model
        app_label = 'app'

    def __str__(self):
        return self.name or f"Leasing Staff Red {self.leasing_staff_red_id}"