from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.utils.translation import gettext_lazy as _
from app.models.time_stamped_model_mixin import TimeStampedModelMixin


class User(AbstractUser , TimeStampedModelMixin):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(_('full name'), max_length=255)
    email = models.EmailField(_('email address'), unique=True) 
    work_phone = models.CharField(max_length=55, blank=True, null=True)
    cell_phone = models.CharField(max_length=55, blank=True, null=True)
    user_company = models.ForeignKey(
        'UserCompany',
        on_delete=models.CASCADE, 
        default=1,
        db_column='user_company_id',
        related_name='users'
    )
    user_role = models.ForeignKey(
        'UserRoles',
        on_delete=models.CASCADE, 
        default=1,
        db_column='user_role_id', 
        related_name='users'
    )
    activated = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    knms_access = models.BooleanField(default=False)


    class Meta(AbstractUser.Meta):
        db_table = 'users'
        app_label = 'app'

    def __str__(self):
        return self.name or self.username or f"User {self.user_id}"


