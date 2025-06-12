from django.db import models
from django.contrib.auth.models import AbstractUser # The base for custom user models
from django.utils.translation import gettext_lazy as _ # For translatable strings



class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)

    # Laravel's 'name' field, often maps to first_name/last_name in AbstractUser.
    # If 'name' is a single field in your DB, keep it.
    # If your DB has 'first_name' and 'last_name', then AbstractUser already covers them.
    # Assuming 'name' is a single field:
    name = models.CharField(_('full name'), max_length=255, blank=True)
    # Remove default AbstractUser fields if you don't use them or they clash with 'name'
    first_name = None # Remove default AbstractUser first_name
    last_name = None  # Remove default AbstractUser last_name

    # Additional fields from Laravel's fillable
    work_phone = models.CharField(max_length=20, blank=True, null=True)
    cell_phone = models.CharField(max_length=20, blank=True, null=True)

    # Relationships from Laravel model
    user_company = models.ForeignKey(
        'UserCompany',
        on_delete=models.SET_NULL, # Assuming user can exist if company is deleted
        null=True, blank=True,
        db_column='user_company_id', # Explicitly map to existing DB column
        related_name='users'
    )
    user_role = models.ForeignKey(
        'UserRoles',
        on_delete=models.SET_NULL, # Assuming user can exist if role is deleted
        null=True, blank=True,
        db_column='user_role_id', # Explicitly map to existing DB column
        related_name='users'
    )

    # Laravel models implicitly handle created_at/updated_at. AbstractUser does not.
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True) # Adding null=True, blank=True if not already
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True) # Adding null=True, blank=True if not already

    class Meta(AbstractUser.Meta): # Inherit Meta options from AbstractUser
        db_table = 'users' # Maps to your existing 'users' table
        app_label = 'app'

    def __str__(self):
        return self.name or self.username or f"User {self.user_id}"

    # You can add custom methods here if needed, like get_full_name if using 'name' field
    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name