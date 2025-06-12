from django.db import models
from .Node import Node                # Import the Node model
from .OntManufacturer import OntManufacturer # Import the OntManufacturer model
from .Home import Home                # Import the Home model

class Ont(models.Model):
    ont_id = models.AutoField(primary_key=True)
    node = models.ForeignKey(
        Node,
        on_delete=models.SET_NULL, # Assuming ONT might remain if Node is deleted
        null=True, blank=True,
        db_column='node_id',
        related_name='onts'
    )
    ont_manufacturer = models.ForeignKey(
        OntManufacturer,
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        db_column='ont_manufacturer_id',
        related_name='ont'
    )
    home = models.OneToOneField( 
        Home,
        on_delete=models.CASCADE, 
        db_column='home_id',
        related_name='ont', 
        null=True, blank=True
    )
    fsan = models.CharField(max_length=255, blank=True, null=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True) 
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    interface = models.CharField(max_length=255, blank=True, null=True)
    model_id = models.CharField(max_length=255, blank=True, null=True) 
    ont_version = models.CharField(max_length=255, blank=True, null=True)
    software_version = models.CharField(max_length=255, blank=True, null=True)
    ont_rx_power = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    olt_rx_power = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    distance = models.IntegerField(blank=True, null=True)
    last_pulled = models.DateTimeField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ont'
        app_label = 'app'

    def __str__(self):
        return f"ONT {self.ont_id} (FSAN: {self.fsan or 'N/A'})"