from django.db import models
from .UserPermissionCategory import UserPermissionCategory     # Import the UserPermissionCategory model
from .UserPermissionSubcategory import UserPermissionSubcategory # Import the UserPermissionSubcategory model

class UserPermissionType(models.Model):
    user_permission_type_id = models.AutoField(primary_key=True)
    user_permission_category = models.ForeignKey(
        UserPermissionCategory,
        on_delete=models.CASCADE, # If category is deleted, its permission types are too
        db_column='user_permission_category_id',
        related_name='permission_types'
    )
    user_permission_subcategory = models.ForeignKey(
        UserPermissionSubcategory,
        on_delete=models.SET_NULL, # Assuming subcategory can be nullable or type remains if subcategory deleted
        null=True, blank=True,
        db_column='user_permission_subcategory_id',
        related_name='permission_types'
    )
    identifier = models.CharField(max_length=255, unique=True) # A unique code/string for the permission type (e.g., 'view_reports')
    description = models.TextField(blank=True, null=True) # A more detailed description of the permission
    # Laravel models often implicitly handle created_at/updated_at. Adding them for completeness.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_permission_type' # Note: Table name is singular as per Laravel model
        app_label = 'app'

    def __str__(self):
        return self.identifier