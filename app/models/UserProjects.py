from django.db import models
from django.contrib.auth import get_user_model

from .Project import Project

User = get_user_model()

class UserProjects(models.Model):
    user_project_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='user_id',
        related_name='user_projects'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        db_column='project_id',
        related_name='user_projects'
    )
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_projects'

    def __str__(self):
        return f"User {self.user_id} assigned to Project {self.project_id}"