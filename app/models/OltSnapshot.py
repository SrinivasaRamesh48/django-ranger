# app/models/OltSnapshot.py
from django.db import models
from .Node import Node


class OltSnapshot(models.Model):
    """Django equivalent of the Laravel OltSnapshot model."""
    node = models.ForeignKey(Node, on_delete=models.CASCADE, db_column='node_id')
    olt_ip_address = models.GenericIPAddressField()
    interface = models.CharField(max_length=100)
    fsan = models.CharField(max_length=100)
    ont_model = models.CharField(max_length=100)
    ont_active_version = models.CharField(max_length=100)
    ont_standby_version = models.CharField(max_length=100)
    ont_rx_power = models.DecimalField(max_digits=5, decimal_places=2)
    ont_tx_power = models.DecimalField(max_digits=5, decimal_places=2)
    distance = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Relationships from Laravel code that imply other tables might link TO this one,
    # but the fillable fields don't contain foreign keys for them.
    # For now, these are not represented as direct ForeignKeys.
    
    class Meta:
        db_table = "olt_snapshot"
        ordering = ['-created_at']