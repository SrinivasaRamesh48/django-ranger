from django.db import models

class UserPermissionCategory(models.Model):
    user_permission_category_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'user_permission_category' 

    def __str__(self):
        return self.description