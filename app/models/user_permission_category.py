from django.db import models
from .time_stamped_model_mixin import TimeStampedModelMixin

class UserPermissionCategory(TimeStampedModelMixin, models.Model):
    user_permission_category_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'user_permission_category' 

    def __str__(self):
        return self.description