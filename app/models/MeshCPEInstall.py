from django.db import models
from .Home import Home # Import the Home model

class MeshCPEInstall(models.Model):
    mesh_cpe_install_id = models.AutoField(primary_key=True)
    home = models.ForeignKey(Home, on_delete=models.CASCADE, db_column='home_id', related_name='mesh_cpe_installs')
    address = models.CharField(max_length=255)
    cpe_id = models.CharField(max_length=255, blank=True, null=True) # CPE ID can be optional/nullable
    cpe_serial_number = models.CharField(max_length=255, blank=True, null=True) # Serial number can be optional/nullable
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Based on the Laravel 'Home' model's 'mesh_installs' relationship
    # having 'whereNull('deleted_at')', it's highly likely this table has a 'deleted_at' field
    deleted_at = models.DateTimeField(null=True, blank=True) # For soft deletes

    class Meta:
        db_table = 'mesh_cpe_installs'
        app_label = 'app'

    def __str__(self):
        return f"Mesh CPE Install {self.mesh_cpe_install_id} for Home {self.home_id}"