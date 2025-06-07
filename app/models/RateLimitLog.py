from django.db import models
from .Home import Home # Import the Home model

class RateLimitLog(models.Model):
    rate_limit_log_id = models.AutoField(primary_key=True)
    home = models.ForeignKey(
        Home,
        on_delete=models.SET_NULL, # Assuming log might remain even if home is deleted
        null=True, blank=True,
        db_column='home_id', # Explicitly map to existing database column
        related_name='rate_limit_logs'
    )
    success = models.BooleanField(default=False)
    rate = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True) # Assuming rate can be a decimal, adjust precision as needed
    result = models.TextField(blank=True, null=True) # For a detailed result message
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rate_limit_log' # Note: Table name is singular as per Laravel model
        app_label = 'app'

    def __str__(self):
        return f"Rate Limit Log {self.rate_limit_log_id} - Success: {self.success}"