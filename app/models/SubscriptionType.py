from django.db import models

class SubscriptionType(models.Model):
    subscription_type_id = models.AutoField(primary_key=True)
    # Assuming this type has a descriptive field, like 'name' for the subscription type.
    name = models.CharField(max_length=255, unique=True) # Common for type tables
    # Add any other fields that might be in your 'subscription_types' table

    class Meta:
        db_table = 'subscription_types'
        app_label = 'app'

    def __str__(self):
        return self.name