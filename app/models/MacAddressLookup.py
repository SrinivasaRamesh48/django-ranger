from django.db import models

class MacAddressLookup(models.Model):
    mac_address_lookup_id = models.AutoField(primary_key=True)
    # Assuming this table stores MAC address prefixes and their manufacturers.
    mac_prefix = models.CharField(max_length=8, unique=True) # E.g., "00-00-00" or "00:00:00" for the OUI
    manufacturer_name = models.CharField(max_length=255)
    # Add any other fields that might be in your 'mac_address_lookup' table

    class Meta:
        db_table = 'mac_address_lookup' # Note: Table name is singular-like as per Laravel model
        app_label = 'app'

    def __str__(self):
        return f"{self.mac_prefix} - {self.manufacturer_name}"