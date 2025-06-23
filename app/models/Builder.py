from django.db import models

class Builder(models.Model):
    builder_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, blank=False) 
    class Meta:
        db_table = 'builders'
        app_label = 'app' 

    def __str__(self):
        return self.name
    
    
