from django.db import models

class UserRoles(models.Model):
    user_role_id = models.AutoField(primary_key=True)
    # Assuming this role has a descriptive field, like 'name'.
    name = models.CharField(max_length=255, unique=True) # Common for role names (e.g., 'Admin', 'Technician')
    # Add any other fields that might be in your 'user_roles' table
    # Laravel models often implicitly handle created_at/updated_at. Adding them for completeness.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_roles'
        app_label = 'app'

    def __str__(self):
        return self.name