from django.db import models
from .time_stamped_model_mixin import TimeStampedModelMixin


class MeshCPEInstall(TimeStampedModelMixin, models.Model):
    mesh_cpe_install_id = models.AutoField(primary_key=True)
    home = models.ForeignKey("Home", on_delete=models.CASCADE, related_name='mesh_installs', db_column='home_id')
    address = models.CharField(max_length=17) # MAC Address
    cpe_id = models.CharField(max_length=100, blank=True, null=True)
    cpe_serial_number = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        db_table = 'mesh_cpe_installs'
        ordering = ['-created_at']