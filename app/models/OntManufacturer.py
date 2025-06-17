from django.db import models
from app.models.TimeStampedModelMixin import TimeStampedModelMixin

class OntManufacturer(TimeStampedModelMixin, models.Model):
    ont_manufacturer_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'ont_manufacturer'
    def __str__(self):
        return f"Manufacturer ID: {self.ont_manufacturer_id}"
