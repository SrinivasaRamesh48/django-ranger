from django.db import models
from django.contrib.auth import get_user_model

from .project import Project
from app.models.time_stamped_model_mixin import TimeStampedModelMixin
User = get_user_model()

class UserProjects(TimeStampedModelMixin, models.Model):
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
   


    class Meta:
        db_table = 'user_projects'

    def __str__(self):
        return f"User {self.user_id} assigned to Project {self.project_id}"