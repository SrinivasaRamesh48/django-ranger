# from django.db import models

# class Circuit(models.Model):
#     circuit_id = models.AutoField(primary_key=True)
#     circuit_carrier = models.ForeignKey('CircuitCarrier', on_delete=models.CASCADE, related_name='circuits', db_column='circuit_carrier_id')
#     title = models.CharField(max_length=255)
#     address = models.TextField(blank=True, null=True)
#     city = models.CharField(max_length=255, blank=True, null=True)
#     state = models.ForeignKey('UsState', on_delete=models.SET_NULL, null=True, related_name='circuits', db_column='state_id')
#     zip_code = models.CharField(max_length=10, blank=True, null=True)
#     circuit_id_a = models.CharField(max_length=255, blank=True, null=True)
#     circuit_id_z = models.CharField(max_length=255, blank=True, null=True)
#     contact_number = models.CharField(max_length=20, blank=True, null=True)
#     activation_date = models.DateField(blank=True, null=True)
#     mbps_speed = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     facility_assignment = models.CharField(max_length=255, blank=True, null=True)
#     media_type = models.CharField(max_length=255, blank=True, null=True)
#     circuit_hub = models.ForeignKey('CircuitHub', on_delete=models.SET_NULL, null=True, related_name='circuits', db_column='circuit_hub_id')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'circuits'
#         app_label = 'app'

#     def __str__(self):
#         return self.title