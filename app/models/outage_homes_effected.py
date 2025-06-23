from django.db import models
from .outage import Outage # Import the Outage model
from .home import Home     # Import the Home model

class OutageHomesEffected(models.Model):
    """Junction table for the Outage-Home Many-to-Many relationship."""
    outage_homes_effected_id = models.AutoField(primary_key=True)
    outage = models.ForeignKey(Outage, on_delete=models.CASCADE, db_column='outage_id')
    home = models.ForeignKey('Home', on_delete=models.CASCADE, db_column='home_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'outage_homes_effected'
        unique_together = ('outage', 'home')