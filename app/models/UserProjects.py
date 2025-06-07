from django.db import models
from django.contrib.auth import get_user_model # Use get_user_model for User

from .Project import Project # Import the Project model

User = get_user_model() # Get the currently active user model

class UserProjects(models.Model):
    user_project_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, # If user is deleted, their project associations are removed
        db_column='user_id',
        related_name='user_projects' # This is the related_name used by User model's projects()
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE, # If project is deleted, its user associations are removed
        db_column='project_id',
        related_name='user_projects'
    )
    # Laravel models often implicitly handle created_at/updated_at. Adding them for completeness.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_projects'
        app_label = 'app'
        # Crucial for junction tables: ensure a user is only associated with a project once
        unique_together = ('user', 'project')

    def __str__(self):
        return f"User {self.user_id} assigned to Project {self.project_id}"