from django.db import models

class CircuitCarrier(models.Model):
    circuit_carrier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    class Meta:
        db_table = 'circuit_carriers'
        app_label = 'app'
  
    def __str__(self):
        return self.name