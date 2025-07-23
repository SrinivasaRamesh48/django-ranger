from rest_framework import serializers
from app.models import MacAddress


class MacAddressSerializer(serializers.ModelSerializer):
    decrypted_ssid = serializers.SerializerMethodField()
    decrypted_passkey = serializers.SerializerMethodField()
    home = serializers.StringRelatedField(read_only=True)
    home_id = serializers.PrimaryKeyRelatedField(
        queryset=MacAddress.objects.all(), source='home', write_only=True
    )
    class Meta:
        model = MacAddress
        fields = [
            'mac_address_id',
            'home',
            'home_id',
            'address',
            'cpe_id',
            'cpe_serial_number',
            'firmware_update',
            'firmware_update_manual',
            'manual_registration',
            'created_at',
            'updated_at',
            # Encrypted fields
            'default_ssid',
            'default_passkey',
            # Decrypted versions
            'decrypted_ssid',
            'decrypted_passkey',
        ]

    def get_home(self, obj):
        if obj.home:
            return {
                'home_id': obj.home.home_id,
                'node_id': obj.home.node.node_id 
            }
        else:
            return None
    def get_decrypted_ssid(self, obj):
        return obj.decrypt_laravel_value(obj.default_ssid)

    def get_decrypted_passkey(self, obj):
        return obj.decrypt_laravel_value(obj.default_passkey)