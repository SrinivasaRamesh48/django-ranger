from django.db import models

class MacAddressLookup(models.Model):
    mac_address_lookup_id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'mac_address_lookup' 
        app_label = 'app'

    def __str__(self):
        return f"{self.mac_prefix} - {self.manufacturer_name}"