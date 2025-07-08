from django.db import models
from .user_permission_type import UserPermissionType
from .user import User
from app.models.time_stamped_model_mixin import TimeStampedModelMixin

class UserPermissions(TimeStampedModelMixin, models.Model):
    user_permission_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    db_column='user_permissions',
    related_name='custom_user_permissions',     
    related_query_name='custom_user_permission'  
)
    user_permission_type = models.ForeignKey(
        UserPermissionType,
        on_delete=models.CASCADE, 
        db_column='user_permission_type_id',
        related_name='user_permissions'
    )

    class Meta:
        db_table = 'user_permissions'
        app_label = 'app'

    def __str__(self):
        return f"User {self.user_id} has Permission Type {self.user_permission_type_id}"