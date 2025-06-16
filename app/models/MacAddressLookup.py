from django.db import models

class MacAddressLookup(models.Model):
    mac_address_lookup_id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'mac_address_lookup' 
        app_label = 'app'

    def __str__(self):
        return f"{self.mac_prefix} - {self.manufacturer_name}"
    
# CREATE TABLE `mac_address_lookup` (
#   `mac_address_lookup_id` int(11) NOT NULL AUTO_INCREMENT,
#   `mac_address` varchar(8) DEFAULT NULL,
#   `manufacturer` varchar(50) DEFAULT NULL,
#   PRIMARY KEY (`mac_address_lookup_id`),
#   KEY `mac_address` (`mac_address`)
# ) ENGINE=InnoDB AUTO_INCREMENT=151638 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
# /*!40101 SET character_set_client = @saved_cs_client */;    