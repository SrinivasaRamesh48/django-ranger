from django.db import models
from app.models import Home  # Assuming Home model is defined in app.models
class RateLimitLog(models.Model):
    """Django equivalent of the Laravel RateLimitLog model."""
    rate_limit_log_id = models.AutoField(primary_key=True)
    home = models.ForeignKey(Home, on_delete=models.CASCADE, db_column='home_id')
    success = models.BooleanField()
    rate = models.CharField(max_length=255)
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rate_limit_log'
        