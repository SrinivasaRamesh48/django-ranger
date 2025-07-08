from django.db import models
from .time_stamped_model_mixin import TimeStampedModelMixin


class Outage(TimeStampedModelMixin, models.Model):
    """Django equivalent of the Laravel Outage model."""
    outage_id = models.AutoField(primary_key=True)
    resolved = models.BooleanField(default=False)
    email_notices_sent = models.BooleanField(default=False)
    phone_notices_sent = models.BooleanField(default=False)
    phone_message_updated = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, db_column='project_id')
    effected_homes = models.ManyToManyField('Home', through='OutageHomesEffected', related_name='outages')
   
    class Meta:
        db_table = "outages"
    def __str__(self):
        return f"Outage {self.outage_id}"