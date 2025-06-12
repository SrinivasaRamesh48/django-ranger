from django.db import models
from .Home import Home         # Import the Home model
from .Subscriber import Subscriber # Import the Subscriber model

class MultiHomeSubscriberHome(models.Model):
    multi_home_subscriber_home_id = models.AutoField(primary_key=True)
    home = models.ForeignKey(
        Home,
        on_delete=models.CASCADE, # If the home is deleted, this link is removed
        db_column='home_id',
        related_name='multi_home_subscriber_homes'
    )
    subscriber = models.ForeignKey(
        Subscriber,
        on_delete=models.CASCADE, # If the subscriber is deleted, this link is removed
        db_column='subscriber_id',
        related_name='multi_home_subscriber_homes'
    )
    created_at = models.DateTimeField(auto_now_add=True) # Assuming these exist in your table
    updated_at = models.DateTimeField(auto_now=True) # Assuming these exist in your table

    class Meta:
        db_table = 'multi_home_subscriber_homes'
        app_label = 'app'
        

    def __str__(self):
        return f"Multi-Home Link: Home {self.home_id} - Subscriber {self.subscriber_id}"