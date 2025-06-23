from django.db import models
from app.models import Home
from app.models.time_stamped_model_mixin import TimeStampedModelMixin
class RateLimitLog(TimeStampedModelMixin, models.Model):
    """Django equivalent of the Laravel RateLimitLog model."""
    rate_limit_log_id = models.AutoField(primary_key=True)
    home = models.ForeignKey(Home, on_delete=models.CASCADE, db_column='home_id')
    success = models.BooleanField()
    rate = models.CharField(max_length=255)
    result = models.TextField()

    class Meta:
        db_table = 'rate_limit_log'
        