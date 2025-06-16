from django.db import models
from .Home import Home         # Import the Home model
from .Subscriber import Subscriber # Import the Subscriber model
from .TimeStampedModelMixin import TimeStampedModelMixin

class MultiHomeSubscriberHome(TimeStampedModelMixin, models.Model):
    """Junction table for the Home-Subscriber Many-to-Many relationship."""
    multi_home_subscriber_home_id = models.AutoField(primary_key=True)
    home = models.ForeignKey(Home, on_delete=models.CASCADE, db_column='home_id')
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, db_column='subscriber_id')
    class Meta:
        db_table = 'multi_home_subscriber_homes'
        unique_together = ('home', 'subscriber') 