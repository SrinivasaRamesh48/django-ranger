from django.db import models
from app.models.time_stamped_model_mixin import TimeStampedModelMixin
class QBOToken(TimeStampedModelMixin, models.Model):
    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_in = models.IntegerField()
    token_type = models.CharField(max_length=50)

    
    class Meta:
        db_table = 'qbo_tokens'
        app_label = 'app'

    def __str__(self):
        return f"QBOToken({self.token_type})"
