# app/models/OltSnapshot.py
from django.db import models

class OltSnapshot(models.Model):
    # 'id' is used as primary key in Laravel
    id = models.AutoField(primary_key=True)  # <--- This is 'id'

    # 'node_id' (foreign key)
    node = models.ForeignKey('Node', on_delete=models.SET_NULL, null=True, blank=True, db_column='node_id', related_name='olt_snapshots') # <--- This handles 'node_id'

    # 'olt_ip_address'
    olt_ip_address = models.CharField(max_length=255) # <--- This is 'olt_ip_address'

    # 'interface'
    interface = models.CharField(max_length=255) # <--- This is 'interface'

    # 'fsan'
    fsan = models.CharField(max_length=255) # <--- This is 'fsan'

    # 'ont_model'
    ont_model = models.CharField(max_length=255, blank=True, null=True) # <--- This is 'ont_model'

    # 'ont_active_version'
    ont_active_version = models.CharField(max_length=255, blank=True, null=True) # <--- This is 'ont_active_version'

    # 'ont_standby_version'
    ont_standby_version = models.CharField(max_length=255, blank=True, null=True) # <--- This is 'ont_standby_version'

    # 'ont_rx_power'
    ont_rx_power = models.CharField(max_length=255, blank=True, null=True)  # <--- This is 'ont_rx_power'

    # 'ont_tx_power'
    ont_tx_power = models.CharField(max_length=255, blank=True, null=True)  # <--- This is 'ont_tx_power'

    # 'distance'
    distance = models.CharField(max_length=255, blank=True, null=True)  # <--- This is 'distance'

    # 'created_at'
    created_at = models.DateTimeField(auto_now_add=True) # <--- This is 'created_at'
    updated_at = models.DateTimeField(auto_now=True) # Assuming updated_at also exists based on common Laravel models.

    class Meta:
        db_table = 'olt_snapshot'
        app_label = 'app'

    def __str__(self):
        return f"OLT Snapshot {self.id} - Interface: {self.interface}"