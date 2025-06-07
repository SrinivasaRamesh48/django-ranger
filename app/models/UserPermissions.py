from django.db import models
from django.contrib.auth import get_user_model # Use get_user_model for User

from .UserPermissionType import UserPermissionType # Assuming UserPermissionType model exists

User = get_user_model() 

class UserPermissions(models.Model):
    user_permission_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
    'app.User',
    on_delete=models.CASCADE,
    db_column='user_permissions',
    related_name='custom_user_permissions',     
    related_query_name='custom_user_permission'  
)
    user_permission_type = models.ForeignKey(
        'app.UserPermissionType',
        on_delete=models.CASCADE, # If permission type is deleted, this permission record is removed
        db_column='user_permission_type_id',
        related_name='user_permissions'
    )
    # Laravel models often implicitly handle created_at/updated_at. Adding them for completeness.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_permissions'
        app_label = 'app'
        # Crucial for junction tables: ensure a user only has a permission type once
        unique_together = ('user', 'user_permission_type')

    def __str__(self):
        return f"User {self.user_id} has Permission Type {self.user_permission_type_id}"