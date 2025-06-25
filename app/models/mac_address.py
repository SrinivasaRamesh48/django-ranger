from django.db import models
import base64
from django.db.models.functions import Substr  
from django.core.exceptions import ObjectDoesNotExist  
from .time_stamped_model_mixin import TimeStampedModelMixin
from .mac_address_lookup import MacAddressLookup
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


APP_KEY_BASE64 = "K4cEH4zzn9wKuv3U4DKIb1pQz1vMJu+zKhXYUlzFDEs="  
APP_KEY = base64.b64decode(APP_KEY_BASE64)


class MacAddress(TimeStampedModelMixin, models.Model):
    mac_address_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=17, unique=True)
    cpe_id = models.CharField(max_length=100, blank=True, null=True)
    cpe_serial_number = models.CharField(max_length=100, blank=True, null=True)
    firmware_update = models.BooleanField(default=False)
    firmware_update_manual = models.BooleanField(default=False)
    manual_registration = models.BooleanField(default=False)
    default_ssid = models.CharField(max_length=255, blank=True, null=True)
    default_passkey = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "mac_address"
    def __str__(self):
        return self.address
    @property
    def manufacturer(self):
        if not self.address:
            return None
        try:
        
            prefix = self.address[:8].upper()
            return MacAddressLookup.objects.get(mac_address=prefix).manufacturer
        except MacAddressLookup.DoesNotExist:
            return "Unknown"
        
        
    def decrypt_laravel_value(self, encrypted_b64):
        try:
            data = base64.b64decode(encrypted_b64)
            iv = data[:16]
            ciphertext = data[16:]
            cipher = AES.new(APP_KEY, AES.MODE_CBC, iv)
            return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
        except Exception as e:
            return None

    def default_credentials(self):
        return {
            "ssid": self.decrypt_laravel_value(self.default_ssid),
            "passkey": self.decrypt_laravel_value(self.default_passkey),
        }