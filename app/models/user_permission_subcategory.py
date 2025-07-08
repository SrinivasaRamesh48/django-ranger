from django.db import models
from .user_permission_category import UserPermissionCategory 
from .time_stamped_model_mixin import TimeStampedModelMixin

class UserPermissionSubcategory(TimeStampedModelMixin, models.Model):
    user_permission_subcategory_id = models.AutoField(primary_key=True)
    user_permission_category = models.ForeignKey(
        UserPermissionCategory,
        on_delete=models.CASCADE,
        db_column='user_permission_category_id',
        related_name='subcategories'
    )
    description = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'user_permission_subcategory' 
        app_label = 'app'

    def __str__(self):
        return self.description