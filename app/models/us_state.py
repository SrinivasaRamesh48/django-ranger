from django.db import models

class UsState(models.Model):
    us_state_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    abbr = models.CharField(max_length=8, unique=True)

    class Meta:
        db_table = 'us_states'

    def __str__(self):
        return self.name