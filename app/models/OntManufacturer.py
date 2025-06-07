from django.db import models

class OntManufacturer(models.Model):
    ont_manufacturer_id = models.AutoField(primary_key=True)
    # Assuming this model has a descriptive field, like 'name' for the manufacturer.
    name = models.CharField(max_length=255, unique=True) # Common for lookup tables
    # Add any other fields that might be in your 'ont_manufacturer' table

    class Meta:
        db_table = 'ont_manufacturer' # Note: Table name is singular as per Laravel model
        app_label = 'app'

    def __str__(self):
        return self.name