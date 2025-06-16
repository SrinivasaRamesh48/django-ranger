from django.db import models
from .Node import Node                # Import the Node model
from .OntManufacturer import OntManufacturer # Import the OntManufacturer model
from .Home import Home                # Import the Home model

class Ont(models.Model):
    """Django equivalent of the Laravel Ont model."""
    ont_id = models.AutoField(primary_key=True)
    fsan = models.CharField(max_length=255)
    mac_address = models.CharField(max_length=17)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    interface = models.CharField(max_length=100, blank=True, null=True)
    model_id = models.CharField(max_length=100, blank=True, null=True)
    ont_version = models.CharField(max_length=100, blank=True, null=True)
    software_version = models.CharField(max_length=100, blank=True, null=True)
    ont_rx_power = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    olt_rx_power = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    distance = models.IntegerField(null=True, blank=True)
    last_pulled = models.DateTimeField(null=True, blank=True)

    # Relationships
    home = models.OneToOneField('Home', on_delete=models.CASCADE, db_column='home_id')
    node = models.ForeignKey('Node', on_delete=models.PROTECT, db_column='node_id')
    manufacturer = models.ForeignKey('OntManufacturer', on_delete=models.PROTECT, db_column='ont_manufacturer_id')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ont'
       

    def __str__(self):
        return self.fsan