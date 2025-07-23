from django.db import models 
from app.models.time_stamped_model_mixin import TimeStampedModelMixin

class OutageHomesEffected(TimeStampedModelMixin, models.Model):
    outage_homes_effected_id = models.AutoField(primary_key=True)
    outage = models.ForeignKey('Outage', on_delete=models.CASCADE, db_column='outage_id', related_name='effected')
    home = models.ForeignKey('Home', on_delete=models.CASCADE, db_column='home_id')

    class Meta:
        db_table = 'outage_homes_effected'
        unique_together = ('outage', 'home')