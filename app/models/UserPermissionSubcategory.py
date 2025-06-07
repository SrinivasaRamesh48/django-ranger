from django.db import models
from .UserPermissionCategory import UserPermissionCategory # Import the UserPermissionCategory model

class UserPermissionSubcategory(models.Model):
    user_permission_subcategory_id = models.AutoField(primary_key=True)
    user_permission_category = models.ForeignKey(
        UserPermissionCategory,
        on_delete=models.CASCADE, # If the category is deleted, subcategories are too
        db_column='user_permission_category_id',
        related_name='subcategories'
    )
    description = models.CharField(max_length=255, unique=True) # Assuming a unique descriptive name for the subcategory
    # Laravel models often implicitly handle created_at/updated_at. Adding them for completeness.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_permission_subcategory' # Note: Table name is singular as per Laravel model
        app_label = 'app'

    def __str__(self):
        return self.description