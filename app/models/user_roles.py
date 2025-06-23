from django.db import models

class UserRoles(models.Model):
    user_role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_roles'

    def __str__(self):
        return self.name