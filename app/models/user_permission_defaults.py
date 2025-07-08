from django.db import models
from .user_roles import UserRoles  
from .user_permission_type import UserPermissionType
from .time_stamped_model_mixin import TimeStampedModelMixin

class UserPermissionDefaults(TimeStampedModelMixin, models.Model):
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

    class Meta:
        db_table = 'user_permission_defaults'
        app_label = 'app'


    def __str__(self):
        return f"Role {self.user_role_id} default for Permission Type {self.user_permission_type_id}"