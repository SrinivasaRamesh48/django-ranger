from django.db import models
from django.db.models.functions import Substr  # For substr()
from django.core.exceptions import ObjectDoesNotExist  # For handling manufacturer lookup

# from .Home import Home  # Import if you need Home model
# from .MacAddressLookup import MacAddressLookup  # Import if you need MacAddressLookup model

class MacAddress(models.Model):
    mac_address_id = models.AutoField(primary_key=True)
    home = models.ForeignKey('Home', on_delete=models.SET_NULL, null=True, blank=True, db_column='home_id', related_name='mac_addresses')  # Use string reference if Home is defined later
    address = models.CharField(max_length=255)  # Assuming MAC address is a string
    cpe_id = models.CharField(max_length=255, blank=True, null=True)
    cpe_serial_number = models.CharField(max_length=255, blank=True, null=True)
    firmware_update = models.BooleanField(default=False)
    firmware_update_manual = models.BooleanField(default=False)
    manual_registration = models.BooleanField(default=False)
    default_ssid = models.CharField(max_length=255, blank=True, null=True)
    default_passkey = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mac_address'
        app_label = 'app'

    def __str__(self):
        return self.address

    # Custom methods/properties for Laravel's dynamic relations
    # ---------------------------------------------------------

    # Django doesn't have direct equivalents of Laravel's `hasOne` for these custom methods.
    # We define them as @property methods to mimic the relationship access.

    @property
    def manufacturer(self):
        # Equivalent of Laravel's `MacAddressLookup::where('mac_address', substr($this->address, 0, 8))->first()`
        # This assumes you have a MacAddressLookup model with a 'mac_address' field.
        try:
            from .MacAddressLookup import MacAddressLookup  # Import locally to avoid circular imports if needed
            return MacAddressLookup.objects.filter(mac_address=Substr('address', 1, 8)).first()
        except ObjectDoesNotExist:
            return None # Or raise an exception if you expect it always to exist

    @property
    def default_credentials_info(self): # Renamed to avoid potential conflicts if 'default_credentials' becomes a model field
        # Equivalent of Laravel's `Crypt::decryptString()` - Django doesn't have built-in encryption
        # You'll need to use a suitable Django library or your own decryption function.
        # This example uses a placeholder:
        def decrypt_string(encrypted_string):
            # Replace this with your actual decryption logic
            return encrypted_string  # Placeholder - replace with actual decryption
        if self.default_ssid and self.default_passkey:
            return {"ssid": decrypt_string(self.default_ssid), "passkey": decrypt_string(self.default_passkey)}
        return None  # Or raise an exception if you expect them to always exist