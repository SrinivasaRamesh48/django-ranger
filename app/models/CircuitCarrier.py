from django.db import models

class CircuitCarrier(models.Model):
    circuit_carrier_id = models.AutoField(primary_key=True)
  
    class Meta:
        db_table = 'circuit_carriers'
        app_label = 'app'
