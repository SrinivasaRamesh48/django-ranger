from django.db import models
from .UserRoles import UserRoles  
from .UserPermissionType import UserPermissionType # Assuming UserPermissionType model exists

class UserPermissionDefaults(models.Model):
    user_permission_defaults_id = models.AutoField(primary_key=True)
    user_role = models.ForeignKey(
        UserRoles,
        on_delete=models.CASCADE, 
        db_column='user_role_id',
        related_name='permission_defaults'
    )
    user_permission_type = models.ForeignKey(
        UserPermissionType,
        on_delete=models.CASCADE,
        db_column='user_permission_type_id',
        related_name='permission_defaults'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_permission_defaults'
        app_label = 'app'


    def __str__(self):
        return f"Role {self.user_role_id} default for Permission Type {self.user_permission_type_id}"