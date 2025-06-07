from django.db import models
class AlertType(models.Model):
    alert_type_id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'alert_types'
        app_label = 'app' 

    def __str__(self):
        return f"Alert Type {self.alert_type_id}"