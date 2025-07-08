from django.db import models
from .outage import Outage
from .home import Home    
from .time_stamped_model_mixin import TimeStampedModelMixin

class OutageHomesEffected(TimeStampedModelMixin, models.Model):
    """Junction table for the Outage-Home Many-to-Many relationship."""
    outage_homes_effected_id = models.AutoField(primary_key=True)
    outage = models.ForeignKey(Outage, on_delete=models.CASCADE, db_column='outage_id')
    home = models.ForeignKey('Home', on_delete=models.CASCADE, db_column='home_id')
    
    class Meta:
        db_table = 'outage_homes_effected'
        unique_together = ('outage', 'home')