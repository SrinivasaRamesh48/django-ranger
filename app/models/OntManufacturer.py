from django.db import models


class OntManufacturer(models.Model):
    ont_manufacturer_id = models.AutoField(primary_key=True)
    class Meta:
        db_table = 'ont_manufacturer'
    def __str__(self):
        return f"Manufacturer ID: {self.ont_manufacturer_id}"
