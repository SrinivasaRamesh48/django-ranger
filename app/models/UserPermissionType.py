from django.db import models
from .UserPermissionCategory import UserPermissionCategory     # Import the UserPermissionCategory model
from .UserPermissionSubcategory import UserPermissionSubcategory # Import the UserPermissionSubcategory model

class UserPermissionType(models.Model):
    user_permission_type_id = models.AutoField(primary_key=True)
    user_permission_category = models.ForeignKey(
        UserPermissionCategory,
        on_delete=models.CASCADE,
        db_column='user_permission_category_id',
        related_name='permission_types'
    )
    user_permission_subcategory = models.ForeignKey(
        UserPermissionSubcategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        db_column='user_permission_subcategory_id',
        related_name='permission_types'
    )
    identifier = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_permission_type'
        app_label = 'app'

    def __str__(self):
        return self.identifier