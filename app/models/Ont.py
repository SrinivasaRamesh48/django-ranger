from django.db import models
from app.models.node import Node             
from app.models.ont_manufacturer import OntManufacturer 
from app.models.time_stamped_model_mixin import TimeStampedModelMixin


class Ont(TimeStampedModelMixin, models.Model):

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
    home = models.ForeignKey('Home', on_delete=models.CASCADE, db_column='home_id',related_name='onts')
    node = models.ForeignKey('Node', on_delete=models.PROTECT, db_column='node_id',related_name='onts')
    manufacturer = models.ForeignKey('OntManufacturer', on_delete=models.PROTECT, db_column='ont_manufacturer_id',related_name='onts')

    class Meta:
        db_table = 'ont'
       

    def __str__(self):
        return self.fsan