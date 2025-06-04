from django.db import models

class Builder(models.Model):
    builder_id = models.AutoField(primary_key=True)
    # Add other fields here that correspond to columns in your 'builders' table
    # For example:
    # name = models.CharField(max_length=255)
    # address = models.TextField()

    class Meta:
        db_table = 'builders'
        app_label = 'app' 

    def __str__(self):
        return f"Builder {self.builder_id}" # Or return a more meaningful representation like self.name if you add a name field