from django.db import models

class UsState(models.Model):
    us_state_id = models.AutoField(primary_key=True)
    # Assuming standard fields for a US state. Adjust based on your actual database schema.
    name = models.CharField(max_length=255, unique=True) # Full state name (e.g., 'California')
    abbr = models.CharField(max_length=2, unique=True)   # Two-letter abbreviation (e.g., 'CA')
    # Laravel models often implicitly handle created_at/updated_at. Adding them for completeness.
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'us_states' # Matches your Laravel protected $table
        app_label = 'app'

    def __str__(self):
        return self.name