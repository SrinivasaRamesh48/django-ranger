# from django.db import models
# from .AlertType import AlertType   
# from .user import User # Assuming you have a User model in the same app or specified elsewhere
# from .outage import Outage # Assuming you have an Outage model in the same app or specified elsewhere

# class Alert(models.Model):
#     alert_id = models.AutoField(primary_key=True)
#     alert_type = models.ForeignKey(AlertType, on_delete=models.CASCADE, db_column='alert_type_id')
#     message = models.TextField()
#     active = models.BooleanField(default=True) # Assuming 'active' is a boolean, adjust if it's an integer (0/1)
#     activated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='alerts_activated')
#     deactivated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='alerts_deactivated')
#     updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='alerts_updated')
#     outage = models.ForeignKey(Outage, on_delete=models.SET_NULL, null=True, db_column='outage_id')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'alerts'
#         app_label = 'your_app_name' # Replace 'your_app_name' with the actual name of your Django app

#     def __str__(self):
#         return f"Alert {self.alert_id} - {self.message[:50]}..." # Return a meaningful representation