# app/models/OltSnapshot.py
from django.db import models

class OltSnapshot(models.Model):
    id = models.AutoField(primary_key=True)
    node = models.ForeignKey('Node', on_delete=models.SET_NULL, null=True, blank=True, db_column='node_id', related_name='olt_snapshots')
    olt_ip_address = models.CharField(max_length=255)
    interface = models.CharField(max_length=255) 
    fsan = models.CharField(max_length=255) 
    ont_model = models.CharField(max_length=255, blank=True, null=True)
    ont_active_version = models.CharField(max_length=255, blank=True, null=True)
    ont_standby_version = models.CharField(max_length=255, blank=True, null=True)
    ont_rx_power = models.CharField(max_length=255, blank=True, null=True)
    ont_tx_power = models.CharField(max_length=255, blank=True, null=True)
    distance = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) 


    class Meta:
        db_table = 'olt_snapshot'
        app_label = 'app'

    def __str__(self):
        return f"OLT Snapshot {self.id} - Interface: {self.interface}"