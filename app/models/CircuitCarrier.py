from django.db import models

class CircuitCarrier(models.Model):
    # Based on your Laravel model, the primary key is named 'circuit_id' in its table.
    # However, the foreign key from 'Circuit' points to 'circuit_carrier_id'.
    # This implies that the 'circuit_carriers' table might have a 'circuit_id' column
    # that serves as its PRIMARY KEY, AND a 'circuit_carrier_id' column that serves as a
    # natural key or is simply what other tables reference.
    # Given the Laravel model, we'll map the primary key to 'circuit_id'.
    # If your database table 'circuit_carriers' truly has 'circuit_carrier_id' as its PK,
    # you'd use that here and adjust your Circuit model's FK accordingly.
    circuit_id = models.AutoField(primary_key=True)
    # Add other fields here that correspond to columns in your 'circuit_carriers' table.
    # For example, a name field for the carrier:
    name = models.CharField(max_length=255, unique=True)
    # Add any other relevant fields, e.g.:
    # contact_person = models.CharField(max_length=255, blank=True, null=True)
    # phone_number = models.CharField(max_length=20, blank=True, null=True)
    # website = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'circuit_carriers'
        app_label = 'app'

    def __str__(self):
        # Assuming you add a 'name' field
        return self.name or f"Circuit Carrier {self.circuit_id}"