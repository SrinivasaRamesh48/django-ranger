from django.db import models
from .user_permission_category import UserPermissionCategory # Import the UserPermissionCategory model

class UserPermissionSubcategory(models.Model):
    user_permission_subcategory_id = models.AutoField(primary_key=True)
    user_permission_category = models.ForeignKey(
        UserPermissionCategory,
        on_delete=models.CASCADE,
        db_column='user_permission_category_id',
        related_name='subcategories'
    )
    description = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_permission_subcategory' 
        app_label = 'app'

    def __str__(self):
        return self.description