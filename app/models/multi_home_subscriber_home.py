from django.db import models
from .subscriber import Subscriber # Import the Subscriber model
from .time_stamped_model_mixin import TimeStampedModelMixin

class MultiHomeSubscriberHome(TimeStampedModelMixin, models.Model):
    multi_home_subscriber_home_id = models.AutoField(primary_key=True)
    home = models.ForeignKey('Home', on_delete=models.CASCADE, db_column='home_id')
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, db_column='subscriber_id')
    class Meta:
        db_table = 'multi_home_subscriber_homes'
        unique_together = ('home', 'subscriber') 