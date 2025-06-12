from django.db import models

class OntManufacturer(models.Model):
    ont_manufacturer_id = models.AutoField(primary_key=True)
    # Assuming this model has a descriptive field, like 'name' for the manufacturer.
   

    class Meta:
        db_table = 'ont_manufacturer' # Note: Table name is singular as per Laravel model
        app_label = 'app'
