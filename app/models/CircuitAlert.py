# from django.db import models
# from .AlertType import AlertType  # Import the AlertType model
# from .Circuit import Circuit      # Import the Circuit model
# from .User import User            # Assuming you have a User model at app/models/User.py

# class CircuitAlert(models.Model):
#     circuit_alert_id = models.AutoField(primary_key=True)
#     alert_type = models.ForeignKey(AlertType, on_delete=models.CASCADE, db_column='alert_type_id', related_name='circuit_alerts')
#     circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, db_column='circuit_id', related_name='circuit_alerts')
#     message = models.TextField()
#     active = models.BooleanField(default=True) # Assuming active is a boolean 0/1
#     activated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='activated_by', related_name='circuit_alerts_activated')
#     deactivated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deactivated_by', related_name='circuit_alerts_deactivated')
#     updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', related_name='circuit_alerts_updated')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'circuit_alerts'
#         app_label = 'app'

#     def __str__(self):
#         return f"Circuit Alert {self.circuit_alert_id} for Circuit {self.circuit_id} - {self.message[:50]}..."