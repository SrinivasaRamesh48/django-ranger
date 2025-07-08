from django.db import models

class SubscriptionType(models.Model):
    subscription_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "subscription_types"
    def __str__(self):
        return self.name