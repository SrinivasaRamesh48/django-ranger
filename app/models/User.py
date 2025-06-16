from django.db import models
from django.contrib.auth.models import AbstractUser # The base for custom user models
from django.utils.translation import gettext_lazy as _ # For translatable strings



class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)

    name = models.CharField(_('full name'), max_length=255, blank=True)
    email = models.EmailField(_('email address'), unique=True, blank=True) 
    work_phone = models.CharField(max_length=20, blank=True, null=True)
    cell_phone = models.CharField(max_length=20, blank=True, null=True)
    user_company = models.ForeignKey(
        'UserCompany',
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        db_column='user_company_id',
        related_name='users'
    )
    user_role = models.ForeignKey(
        'UserRoles',
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        db_column='user_role_id', 
        related_name='users'
    )

    # Laravel models implicitly handle created_at/updated_at. AbstractUser does not.
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True) # Adding null=True, blank=True if not already
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True) # Adding null=True, blank=True if not already

    class Meta(AbstractUser.Meta):
        db_table = 'users'

    def __str__(self):
        return self.name or self.username or f"User {self.user_id}"