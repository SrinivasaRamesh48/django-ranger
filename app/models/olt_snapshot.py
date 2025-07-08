# app/models/OltSnapshot.py
from django.db import models
from .node import Node


class OltSnapshot(models.Model):
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

    
    class Meta:
        db_table = "olt_snapshot"
        ordering = ['-created_at']