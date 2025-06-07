from django.db import models

class QBOToken(models.Model):
    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_in = models.IntegerField()
    token_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = 'qbo_tokens'
        app_label = 'app'

    def __str__(self):
        return f"QBOToken({self.token_type})"
