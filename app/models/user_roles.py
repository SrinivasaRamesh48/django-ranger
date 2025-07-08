from django.db import models

class UserRoles(models.Model):
    user_role_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, unique=True)
    dispatch = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        db_table = 'user_roles'

    def __str__(self):
        return self.description