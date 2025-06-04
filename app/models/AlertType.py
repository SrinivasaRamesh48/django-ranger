# from django.db import models
# class AlertType(models.Model):
#     alert_type_id = models.AutoField(primary_key=True)
#     # Add other fields here that correspond to columns in your 'alert_types' table
#     # For example:
#     # name = models.CharField(max_length=255)
#     # description = models.m.TextField()

#     class Meta:
#         db_table = 'alert_types'
#         app_label = 'app' 

#     def __str__(self):
#         return f"Alert Type {self.alert_type_id}" # Or return a more meaningful representation like self.name if you add a name field