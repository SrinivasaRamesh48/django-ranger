from django.db import models
from .Outage import Outage # Import the Outage model
from .Home import Home     # Import the Home model

class OutageHomesEffected(models.Model):
    outage_homes_effected_id = models.AutoField(primary_key=True)
    outage = models.ForeignKey(
        Outage,
        on_delete=models.CASCADE, # If the outage is deleted, this record is removed
        db_column='outage_id',
        related_name='homes_effected' # Access from Outage: outage_instance.homes_effected.all()
    )
    home = models.ForeignKey(
        Home,
        on_delete=models.CASCADE, # If the home is deleted, this record is removed
        db_column='home_id',
        related_name='outages_effecting' # Access from Home: home_instance.outages_effecting.all()
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'outage_homes_effected'
        app_label = 'app'
        # Crucial for junction tables: ensure a home is only linked to an outage once
        unique_together = ('outage', 'home')

    def __str__(self):
        return f"Outage {self.outage_id} affects Home {self.home_id}"